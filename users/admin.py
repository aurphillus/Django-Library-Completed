from django.contrib import admin
from landingpage.models import Quote
from users.models import Profile
# Register your models here.

admin.site.register(Quote)
admin.site.register(Profile)