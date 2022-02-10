from django import template
from django.shortcuts import render, redirect, reverse, get_object_or_404


from users.models import Profile


register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータを一部を置き換える"""

    url_dict = request.GET.copy()
    url_dict[field] = str(value)  # Django2.1の一部対策。通常はvalueだけでOK
    return url_dict.urlencode()

@register.simple_tag
def is_checked(value, checked_item):
    # print(value in checked_item)
    if str(value) in checked_item or value in checked_item:
        return 'checked'
    else:
        return ''

@register.inclusion_tag('inclusion_tag/group_join_link.html', takes_context=True)
def request_user_is_in_the_group(context):
    user_profile = get_object_or_404(Profile, user=context['request'].user)
    inclusion_context = {}



    if context['object'].recruit_member:
        inclusion_context['recruiting_member'] = True

        if user_profile in context['object'].member.all():
            inclusion_context['request_user_is_in_the_group'] = True

        else:
            inclusion_context['request_user_is_in_the_group'] = False
            inclusion_context['object'] = context['object']
    else:
        inclusion_context['recruiting_member'] = False

    return inclusion_context


    # if context['object'].recruit_member and user_profile not in context['object'].member.all():
    #     return {'recruiting_member' : True, 'request_user_is_in_the_group': False, 'object': context['object']}
    # elif not context['object'].recruit_member:
    #     return {'recruiting_member' : False}
    #
    # else:
    #     return {'request_user_is_in_the_group': True}
