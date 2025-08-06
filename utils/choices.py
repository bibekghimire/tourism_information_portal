from django.db import models
from rest_framework.permissions import BasePermission

ROLE_ASSIGNABLE = {
    'SU':['AD','ST', 'CR'],
    'AD': ['ST', 'CR'],
    'ST': ['CR'],
    'CR': []
}

class RoleChoices(models.TextChoices):
    ADMIN= 'AD', 'Admin'
    STAFF= 'ST', 'Staff'
    CREATOR= 'CR', 'Creator'

    @classmethod
    def get_assignable_roles(cls, role):
         return [
            {"value": r, "label": cls(r).label}
            for r in ROLE_ASSIGNABLE.get(role, [])
        ]

class StatusChoices(models.TextChoices):
    ACTIVE='ACT', 'Active'
    SUSPENDED= 'SUS', 'Suspended'
    DELETED= 'DEL', 'Deleted'

