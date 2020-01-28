from django.contrib import admin
from .models import Application, Landmark, Profile, Contact

admin.site.register(Application)
admin.site.register(Landmark)
admin.site.register(Profile)
admin.site.register(Contact)