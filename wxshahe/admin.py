from django.contrib import admin

# Register your models here.
from .models import User
from .models import Diet
from .models import Cook
from .models import Log
from .models import Attribution
from .models import Group
admin.site.register(User)
admin.site.register(Diet)
admin.site.register(Cook)
admin.site.register(Log)
admin.site.register(Attribution)
admin.site.register(Group)
