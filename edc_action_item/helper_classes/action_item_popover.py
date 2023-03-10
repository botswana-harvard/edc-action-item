from urllib.parse import urlparse, parse_qsl

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_base import convert_php_dateformat
from edc_constants.constants import OPEN

from edc_action_item import site_action_items, HIGH_PRIORITY
from edc_action_item.choices import ACTION_STATUS


class ActionItemPopover:
    def __init__(self, action_item_model_wrapper, tabindex):
        self.action_item_model_wrapper = action_item_model_wrapper
        self.tabindex = tabindex

    def model_fk(self, action_item_obj=None):
        ref_model_a = settings.PARENT_REFERENCE_MODEL1
        ref_model_b = settings.PARENT_REFERENCE_MODEL2
        if ref_model_a and ref_model_b:
            if action_item_obj.parent_reference_model == ref_model_a:
                app_label, model_name = ref_model_a.split('.')
                mdl_cls = django_apps.get_model(app_label, model_name)
                try:
                    obj = mdl_cls.objects.get(
                        subject_identifier=action_item_obj.subject_identifier,
                        tracking_identifier=action_item_obj.parent_reference_identifier)
                    return {settings.ACTION_ITEM_MODEL_FK_FIELD: getattr(obj, 'pk')}
                except mdl_cls.DoesNotExist:
                    pass
            elif action_item_obj.parent_reference_model == ref_model_b:
                app_label, model_name = ref_model_b.split('.')
                mdl_cls = django_apps.get_model(app_label, model_name)
                try:
                    obj = mdl_cls.objects.get(
                        subject_identifier=action_item_obj.subject_identifier,
                        tracking_identifier=action_item_obj.parent_reference_identifier)
                    field_name = settings.ACTION_ITEM_MODEL_FK_FIELD
                    return {
                        settings.ACTION_ITEM_MODEL_FK_FIELD: getattr(obj, field_name).pk}
                except mdl_cls.DoesNotExist:
                    pass
            else:
                return
        return

    @property
    def generate_popover_dict(self):
        strike_thru = None
        action_item = self.action_item_model_wrapper.object
        href = self.action_item_model_wrapper.href
        date_format = convert_php_dateformat(settings.SHORT_DATE_FORMAT)

        if action_item.last_updated:
            last_updated = action_item.last_updated.strftime(date_format)
            user_last_updated = action_item.user_last_updated
            last_updated_text = (
                f'Last updated on {last_updated} by {user_last_updated}.')
        else:
            last_updated_text = 'This action item has not been updated.'

        # this reference model and url
        reference_model_cls = django_apps.get_model(action_item.action_type.model)
        query_dict = dict(parse_qsl(urlparse(href).query))
        model_fk_dict = self.model_fk(action_item_obj=action_item)
        if model_fk_dict:
            query_dict.update(model_fk_dict)
        parent_reference_model_url = None
        parent_reference_model_name = None
        action_item_reason = None
        parent_action_identifier = None
        # reference_model and url
        action_cls = site_action_items.get(reference_model_cls.action_name)
        try:
            reference_model_obj = reference_model_cls.objects.get(
                action_identifier=action_item.action_identifier)
        except ObjectDoesNotExist:
            reference_model_obj = None
        try:
            subject_visit = reference_model_obj.visit
        except (AttributeError, ObjectDoesNotExist):
            pass
        else:
            # reference model is a CRF, add visit to querystring
            query_dict.update({
                reference_model_obj.visit_model_attr(): str(subject_visit.pk),
                'appointment': str(subject_visit.appointment.pk)})
        try:
            reference_model_url = action_cls.reference_model_url(
                action_item=action_item,
                action_identifier=action_item.action_identifier,
                reference_model_obj=reference_model_obj,
                **query_dict)
        except ObjectDoesNotExist:
            reference_model_url = None
            # object wont exist if an action item was deleted
            # that was created by another action item.
            strike_thru = True
        else:
            if action_item.parent_action_item:

                # parent action item
                parent_reference_model_cls = django_apps.get_model(
                    action_item.parent_action_item.action_type.model)

                # parent reference model and url
                try:
                    parent_reference_model_obj = parent_reference_model_cls.objects.get(
                        tracking_identifier=action_item.parent_action_item.reference_identifier)

                except ObjectDoesNotExist:
                    pass
                else:
                    try:
                        subject_visit = parent_reference_model_obj.visit
                    except (AttributeError, ObjectDoesNotExist):
                        pass
                    else:
                        # parent reference model is a CRF, add visit to querystring
                        query_dict.update({
                            parent_reference_model_obj.visit_model_attr(): str(
                                subject_visit.pk),
                            'appointment': str(subject_visit.appointment.pk)})
                    parent_reference_model_url = (
                        action_cls.reference_model_url(
                            reference_model_obj=parent_reference_model_obj,
                            action_item=action_item,
                            action_identifier=action_item.action_identifier,
                            **query_dict))

                    parent_reference_model_name = (
                        f'{parent_reference_model_cls._meta.verbose_name} '
                        f'{parent_reference_model_obj.tracking_identifier}')
                    action_item_reason = parent_reference_model_obj.action_item_reason
                parent_action_identifier = action_item.parent_action_item.action_identifier

        open_display = [c[1] for c in ACTION_STATUS if c[0] == OPEN][0]

        return dict(
            HIGH_PRIORITY=HIGH_PRIORITY,
            OPEN=open_display,
            action_instructions=action_item.instructions,
            action_item_reason=action_item_reason,
            report_datetime=action_item.report_datetime,
            display_name=action_item.action_type.display_name,
            action_identifier=action_item.action_identifier,

            parent_action_identifier=parent_action_identifier,
            parent_action_item=action_item.parent_action_item,

            href=href,
            last_updated_text=last_updated_text,
            name=action_item.action_type.name,

            reference_model_name=reference_model_cls._meta.verbose_name,
            reference_model_url=reference_model_url,
            reference_model_obj=reference_model_obj,
            action_item_color=action_cls.color_style,

            parent_model_name=parent_reference_model_name,
            parent_model_url=parent_reference_model_url,

            priority=action_item.priority or '',
            status=action_item.get_status_display(),
            tabindex=self.tabindex,
            strike_thru=strike_thru)
