from rest_framework import permissions


class IsCourseAuthor(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):  # obj=запись из бд
        return request.user == obj.owner
