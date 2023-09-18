from io import StringIO
from logging import StringTemplateStyle
from django.utils.text import slugify
import random
import string
def generate_slug( instance, base_title, new_slug=False, update=False):
    slug = slugify(base_title)
    model = instance.__class__
    if new_slug:
        slug = new_slug

    if update : 
        slug_exists = model.objects.filter(
            slug__icontains = slug
        ).exclude(pk=instance.pk)

    else:
        slug_exists = model.objects.filter(
            slug__icontains = slug
        ).exists()

    if slug_exists:
        random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
        new_slug = slugify(f"{base_title} {random_string}")
        return generate_slug(instance, base_title, new_slug=new_slug)
    

    return slug