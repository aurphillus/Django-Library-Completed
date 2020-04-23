import random
from django.utils.text import slugify


def unique_slug_generator(title):
    slug = slugify(title)

    return slug