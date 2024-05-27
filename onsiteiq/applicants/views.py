import json

from django.core.exceptions import PermissionDenied, ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers

from applicants.services.applicant_service import ApplicantService
from applicants.services.permission_service import PermissionService


@csrf_exempt
def login(request):
    """
    Logs in a user of this API, enabling them to access the rest of the functionality,
    assuming they have permission to do so.

    NOTE: This is absolutely not what I would do in production, ideally we would
    separate this concern into its own middleware
    :param request:
    :return:
    """
    user = PermissionService.authenticate_and_login_request(request)
    if user is None:
        raise PermissionDenied()

    return JsonResponse({
        "msg": "User login success"
    })


@csrf_exempt
@login_required
@permission_required('applicants.can_create_applicant')
def create(request) -> HttpResponse:
    """
    Interface for creating new applicants. Acts as an interface for Applicant Service
    which houses actual logic for applicant creation.
    :param request:
    :return: HttpResponse with created applicant json
    """
    create_fields = json.loads(request.body)

    # Cheap way to validate, if this was to scale/go into prod we would obviously
    # need standalone validators
    if not (
        set(create_fields.keys()) == {"first_name", "last_name", "email_address", "phone_number"} and
        all([True for val in create_fields.values() if val])
    ):
        raise ValidationError

    created_applicant = ApplicantService.create_applicant(create_fields)
    data = serializers.serialize('json', [created_applicant])
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required
@permission_required('applicants.can_view_applicant')
def view_all(request) -> HttpResponse:
    """
    Interface to query all current applicants. This acts as an interface for
    the underlying Applicant Service which does the heavy lifting
    :param request: Http Request with all required params
    :return: Http Response with representation of all Applicants
    """
    all_applicants = ApplicantService.get_all_applicants()
    data = serializers.serialize('json', all_applicants)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required
@permission_required('applicants.can_view_applicant')
def view_one(request, unique_id: str) -> HttpResponse:
    """
    Interface to view single Applicant. Interfaces with underlying service
    :param request: Http Request with all required params
    :param unique_id: uuid of target applicant
    :return: Http Response with applicant representation, if there was one
    """
    applicant = ApplicantService.get_one_applicant(unique_id)
    data = serializers.serialize('json', [applicant])
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required
@permission_required('applicants.can_create_update_note')
def update_note(request, unique_id: str) -> HttpResponse:
    """
    Endpoint to update single applicant's note. Interface with underlying service that does
    the heavy lifting
    :param request: Http Request with all required params
    :param unique_id: id of what we're updating
    :return: boolean of whether this was updated
    """
    post_fields = json.loads(request.body)
    note = post_fields.get("note")
    was_updated = ApplicantService.update_note(unique_id, note)

    return HttpResponse({"was_updated": was_updated}, content_type='application/json')


@csrf_exempt
@login_required
@permission_required('applicants.can_accept_reject_applicant')
def approve_reject(request, unique_id: str) -> HttpResponse:
    """
    Endpoint to update single applicant's approval. Interface with underlying service that does
    the heavy lifting
    :param request: Http Request with all required params
    :param unique_id: id of what we're updating
    :return: boolean of whether this was updated
    """
    post_fields = json.loads(request.body)
    approval_status = post_fields.get("approval_status")

    # Extremely jank validation, I usually have django rest framework validators do this
    if not isinstance(approval_status, bool):
        raise Exception("Malformed approval status!")

    approval_status = bool(approval_status)
    was_updated = ApplicantService.approve_or_reject(unique_id, approval_status)

    return HttpResponse({"was_updated": was_updated}, content_type='application/json')


