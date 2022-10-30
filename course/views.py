from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, response
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rating.serializers import ReviewSerializer
from .models import Course, Category, WhatYouLearn, Requirements
from . import serializers
from rest_framework.pagination import PageNumberPagination
from .serializers import WhatYouLearnSerializer, RequirementsSerializer
from .service import CourseFilter
from rest_framework.decorators import action
from rating.models import Favorite


class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 1000


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    queryset = Category.objects.all()
    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class CourseViewSet(ModelViewSet):
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    queryset = Course.objects.all()
    filterset_class = CourseFilter
    search_fields = ['price']
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CourseListSerializer
        return serializers.CourseDetailSerializer

    # api/v1/courses/<id>/what_learn/
    # @action(['GET', 'POST'], detail=True)
    # def what_learn(self, request, pk):
    #     course = self.get_object()
    #     if request.method == 'GET':
    #         what_learn = course.what_learn.all()
    #         serializer = WhatYouLearnSerializer(what_learn, many=True)
    #         return response.Response(serializer.data, status=200)
    #     data = request.data
    #     serializer = WhatYouLearnSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(course=course)
    #     return response.Response(serializer.data, status=201)

    # api/v1/courses/<id>/requirements/
    @action(['GET', 'POST'], detail=True)
    def requirements(self, request, pk):
        course = self.get_object()
        if request.method == 'GET':
            requirements = course.requirements.all()
            serializer = RequirementsSerializer(requirements, many=True)
            return response.Response(serializer.data, status=200)
        data = request.data
        serializer = RequirementsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return response.Response(serializer.data, status=201)

    # api/v1/courses/<id>/reviews/
    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk):
        course = self.get_object()
        if request.method == 'GET':
            reviews = course.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return response.Response(serializer.data, status=200)
        if course.reviews.filter(owner=request.user).exists():
            return response.Response('Вы уже оставляли отзыв!', status=400)
        data = request.data
        serializer = ReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user, course=course)
        return response.Response(serializer.data, status=201)

    @action(['POST'], detail=True)
    def favorite_action(self, request, pk):
        course = self.get_object()
        user = request.user
        if user.favorites.filter(course=course).exists():
            user.favorites.filter(course=course).delete()
            return Response('Deleted From Favorites!', status=204)
        Favorite.objects.create(owner=user, course=course)
        return Response('Added to Favorites!', status=201)


# class WhatYouLearnViewSet(ModelViewSet):
#     queryset = WhatYouLearn.objects.all()
#     serializer_class = serializers.WhatYouLearnSerializer
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         return [IsCourseAuthor()]
#
#
# class RequirementsViewSet(ModelViewSet):
#     queryset = Requirements.objects.all()
#     serializer_class = serializers.RequirementsSerializer
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         return [IsCourseAuthor()]

# TODO action['put', 'delete']gi