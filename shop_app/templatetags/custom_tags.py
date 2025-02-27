from django import template

register = template.Library()


@register.filter
def make_groups(value, group_size):
    """
    ক্যাটেগরিগুলোকে নির্দিষ্ট সংখ্যক গ্রুপে ভাগ করবে।
    উদাহরণ: make_groups(categories, 3)
    """
    group_size = int(group_size)
    return [value[i:i + group_size] for i in range(0, len(value), group_size)]
