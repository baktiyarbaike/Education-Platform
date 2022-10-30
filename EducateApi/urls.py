
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from EducateApi import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from course.views import CourseViewSet, CategoryViewSet
from rap.views import auth
from rating.views import ReviewViewSet

# Для Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Eduction_platform test project",
      default_version='v1',
      description="Test REST API backend at django",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Роутеры для вьюшек
router = SimpleRouter()
router.register('courses', CourseViewSet)
router.register('categories', CategoryViewSet)
router.register('reviews', ReviewViewSet)
# router.register('course/<int:pk>/what_learn', WhatYouLearnViewSet)
# router.register('course/<int:pk>/requirements', RequirementsViewSet),

# Основные urls
urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('', include('social_django.urls', namespace='social')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('rap.urls')),
    path('api/v1/', include(router.urls)),
    path('auth/', auth),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
