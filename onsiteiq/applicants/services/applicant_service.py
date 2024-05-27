from typing import Dict, Iterable
from applicants.models import Applicant


class ApplicantService:
    """
    Straightforward service to house business logic related to updating/creating/reading
    Applicant objects.

    Note: In a production app I like putting business logic in a standalone service like
    this and leave "guardrails"/other basic checks on the model. Given the scope
    here I'm just putting everything on this service.
    """

    @classmethod
    def create_applicant(cls, new_applicant_fields: Dict[str, str]) -> Applicant:
        created = Applicant.objects.create(
            **new_applicant_fields
        )
        return created

    @classmethod
    def get_all_applicants(cls) -> Iterable[Applicant]:
        return Applicant.objects.all()

    @classmethod
    def get_one_applicant(cls, applicant_id: str) -> Applicant:
        applicant = Applicant.objects.get(unique_id=applicant_id)
        return applicant

    @classmethod
    def update_note(cls, applicant_id: str, note_msg: str) -> bool:
        applicant = Applicant.objects.get(unique_id=applicant_id)
        applicant.note = note_msg
        applicant.save(update_fields=["note"])

        return True

    @classmethod
    def approve_or_reject(cls, applicant_id: str, approval_status: bool) -> bool:
        applicant = Applicant.objects.get(unique_id=applicant_id)
        applicant.approval_status = approval_status
        applicant.save(update_fields=["approval_status"])

        return True
