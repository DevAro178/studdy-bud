from django.contrib import admin

# Register your models here.
from .models import Room
from .models import Topic
from .models import Message
from .models import User

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)