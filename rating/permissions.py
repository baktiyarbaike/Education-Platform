from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner    # request.user=юзер, который отправил запрос, obj.owner=юзер, который создал эту запись в бд