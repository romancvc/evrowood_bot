from django.contrib import admin

from .forms import ProfileForm
from .models import Profile
from .models import User
from .models import Questions
from .models import UserQuestions
from .models import PointSales

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'nickname')
    form = ProfileForm

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'key_auto')

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('quest_id', 'name_quest')

@admin.register(UserQuestions)
class UserQuestionsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'quest_id', 'date_ad', 'date_comletion', 'completed')

@admin.register(PointSales)
class PointSalesAdmin(admin.ModelAdmin):
    list_display = ('point_id', 'point_name', 'point_address', 'contacts_point_name', 'contacts_point_phone')
