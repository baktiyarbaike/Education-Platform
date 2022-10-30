from django.contrib import admin
from .models import Category, Course, Level, Requirements, WhatYouLearn


class WhatYouLearnTabInline(admin.TabularInline):
    model = WhatYouLearn


class RequirementsTabInline(admin.TabularInline):
    model = Requirements


class CourseAdmin(admin.ModelAdmin):
    inlines = (WhatYouLearnTabInline, RequirementsTabInline)


admin.site.register(Level)
admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(WhatYouLearn)
admin.site.register(Requirements)


# @admin.register(Course)
# class Course(admin.ModelAdmin):
#     list_display = ('owner', 'title', 'image', 'CourseAdmin')