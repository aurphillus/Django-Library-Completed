import random
from django.utils.text import slugify

def unique_slug_generator_author(name):
    first_name = name.strip().split(' ')[0]
    last_name = ' '.join((name + ' ').split(' ')[1:]).strip()
    
    if first_name and last_name:
        name = first_name+ ' '+last_name
    elif first_name and not last_name:
        name = first_name
    elif last_name and not first_name:
        name = last_name
    
    str = replace_all(name.lower())
    slug = slugify(str)
    
    return slug
def replace_all(text):
    rep = {
        'ı':'i',
        'ş':'s',
        'ü':'u',
        'ö':'o',
        'ğ':'g',
        'ç':'c'
    }
    for i, j in rep.items():
            text = text.replace(i, j)
    return text