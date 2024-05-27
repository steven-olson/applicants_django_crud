import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth.models import Permission

from applicants.models import Applicant


class TestApplicantView(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="joe")
        self.user.set_password("Test1!23")
        self.user.save(update_fields=["password"])
        self.client = Client()
        self.client.login(username=self.user.username, password=self.user.password)
        self.login_and_authenticate()

    def refresh_client(self):
        self.user.refresh_from_db()
        self.client = Client()
        self.client.login(username=self.user.username, password="Test1!23")

    def login_and_authenticate(self):
        res = self.client.post(
            "/applicants/login/",
            data=json.dumps({
                "username": self.user.username,
                "password": "Test1!23"
            }),
            content_type="application/json"
        )

    def tearDown(self):
        # Only doing this for local testing to make use of --keepdb, obviously we wouldnt do this in
        # ci/cd tests
        Applicant.objects.all().delete()

    def test_create(self):
        # Try creating a new user without permissions
        no_perm_res = self.client.post(
            "/applicants/create/",
            data=json.dumps({
                "first_name": "mike",
                "last_name": "asd",
                "email_address": "test@test.com",
                "phone_number": "123-456-7890"
            }),
            content_type="application/json"
        )
        self.assertEqual(no_perm_res.status_code, 302)

        # Now lets give our user permission and try again
        create_permission = Permission.objects.get(codename="can_create_applicant")
        self.user.user_permissions.add(create_permission)
        self.refresh_client()
        res = self.client.post(
            "/applicants/create/",
            data=json.dumps({
                "first_name": "mike",
                "last_name": "asd",
                "email_address": "test@test.com",
                "phone_number": "123-456-7890"
            }),
            content_type="application/json"
        )
        # Make sure response looks good
        self.assertEqual(res.status_code, 200)
        created_fields = json.loads(res.content)[0]["fields"]

        created_model = Applicant.objects.last()
        self.assertTrue(created_model.first_name == "mike" == created_fields["first_name"])
        self.assertTrue(created_model.last_name == "asd" == created_fields["last_name"])
        self.assertTrue(created_model.email_address == "test@test.com" == created_fields["email_address"])
        self.assertTrue(created_model.phone_number == "123-456-7890" == created_fields["phone_number"])

    def test_view_all(self):
        # Create a few applicants
        Applicant.objects.create(first_name="joe", last_name="smith", phone_number="123-456-7890")
        Applicant.objects.create(first_name="steve", last_name="smith", phone_number="123-456-7890")
        Applicant.objects.create(first_name="mike", last_name="smith", phone_number="123-456-7890")

        # Try reading without permissions
        no_perm_res = self.client.get(
            "/applicants/view_all/",
        )
        self.assertEqual(no_perm_res.status_code, 302)

        # Now lets give our user permission and try again
        create_permission = Permission.objects.get(codename="can_view_applicant")
        self.user.user_permissions.add(create_permission)
        self.refresh_client()
        res = self.client.get(
            "/applicants/view_all/",
        )

        # Make sure output looks good
        self.assertEqual(res.status_code, 200)
        created_fields = [json_res["fields"] for json_res in json.loads(res.content)]

        for created_field in created_fields:
            matching = Applicant.objects.get(first_name=created_field["first_name"])
            self.assertTrue(matching is not None)

    def test_view_one(self):
        # Create test applicant
        created_applicant = Applicant.objects.create(first_name="joe", last_name="smith", phone_number="123-456-7890")

        # Try hitting endpoint w/o auth
        no_perm_res = self.client.get(
            f"/applicants/view/{str(created_applicant.unique_id)}/",
        )
        self.assertEquals(no_perm_res.status_code, 302)

        # Try again with perms
        create_permission = Permission.objects.get(codename="can_view_applicant")
        self.user.user_permissions.add(create_permission)
        self.refresh_client()
        res = self.client.get(
            f"/applicants/view/{str(created_applicant.unique_id)}/",
        )

        # Make sure response looks good
        created_fields = json.loads(res.content)[0]["fields"]
        self.assertEquals(created_fields["unique_id"], str(created_applicant.unique_id))

    def test_update_note(self):
        created_applicant = Applicant.objects.create(first_name="joe", last_name="smith", phone_number="123-456-7890")
        # Try hitting endpoint w/o auth
        no_perm_res = self.client.post(
            f"/applicants/note/{str(created_applicant.unique_id)}/",
            data=json.dumps({
                "note": "hello im a note"
            }),
            content_type="application/json"
        )
        self.assertEquals(no_perm_res.status_code, 302)

        # Try again with perms
        create_permission = Permission.objects.get(codename="can_create_update_note")
        self.user.user_permissions.add(create_permission)
        self.refresh_client()
        res = self.client.post(
            f"/applicants/note/{str(created_applicant.unique_id)}/",
            data=json.dumps({
                "note": "hello im a note"
            }),
            content_type="application/json"
        )

        created_applicant.refresh_from_db()
        self.assertEquals(created_applicant.note, "hello im a note")

    def test_approve_reject(self):
        created_applicant = Applicant.objects.create(first_name="joe", last_name="smith", phone_number="123-456-7890")
        # Try hitting endpoint w/o auth
        no_perm_res = self.client.post(
            f"/applicants/approve_reject/{str(created_applicant.unique_id)}/",
            data=json.dumps({
                "approval_status": True
            }),
            content_type="application/json"
        )
        self.assertEquals(no_perm_res.status_code, 302)

        # Try again with perms
        create_permission = Permission.objects.get(codename="can_accept_reject_applicant")
        self.user.user_permissions.add(create_permission)
        self.refresh_client()
        res = self.client.post(
            f"/applicants/approve_reject/{str(created_applicant.unique_id)}/",
            data=json.dumps({
                "approval_status": True
            }),
            content_type="application/json"
        )
        self.assertEquals(res.status_code, 200)

        created_applicant.refresh_from_db()
        self.assertEquals(created_applicant.approval_status, True)
