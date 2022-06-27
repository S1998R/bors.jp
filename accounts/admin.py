from django.contrib import admin

from .models import CustomUser, Initial, University, Faculty, Department


class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email', 'id')
    list_display = ('username', 'email', 'id')
    list_filter = ('username', 'email', 'id')


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'faculty', )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Initial)
admin.site.register(University)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)
