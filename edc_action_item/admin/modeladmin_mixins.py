from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)

from .exportaction_mixin import ExportActionMixin


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin, ModelAdminRedirectOnDeleteMixin,
                      ExportActionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
