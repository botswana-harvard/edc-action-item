from django import template

from edc_action_item.helper_classes.action_item_popover import ActionItemPopover
from ..site_action_items import site_action_items

register = template.Library()


@register.inclusion_tag('edc_action_item/add_action_item_popover.html')
def add_action_item_popover(subject_identifier, subject_dashboard_url):
    action_item_add_url = (
        'edc_action_item_admin:edc_action_item_actionitem_add')
    show_link_to_add_actions = site_action_items.get_show_link_to_add_actions()
    return dict(
        action_item_add_url=action_item_add_url,
        subject_identifier=subject_identifier,
        subject_dashboard_url=subject_dashboard_url,
        show_link_to_add_actions=show_link_to_add_actions)


@register.inclusion_tag('edc_action_item/action_item_with_popover.html')
def action_item_with_popover(action_item_model_wrapper, tabindex):
    action_popover = ActionItemPopover(
        action_item_model_wrapper=action_item_model_wrapper, tabindex=tabindex)

    return action_popover.generate_popover_dict
