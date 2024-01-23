"""
URL configuration for PersonalityPrediction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from resumeuploads.views import (upload_document, resume_home, resume_jobs,
                                 resume_mbti, tmp_view, resume_info, sse_view)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('resumeuploads.urls')),
    path('upload/', upload_document, name='upload'),
    path('resume-home/', resume_home, name='resume-home'),
    # path('', resume_home, name='home'),
    path('resume-mbti/', resume_mbti, name='resume-mbti'),
    path('resume-info/', resume_info, name='resume-info'),
    path('resume-jobs/', resume_jobs, name='resume-jobs'),
    path('tmp/', tmp_view, name='tmp'),

    # Django rest framework
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Tests
    path('tmp/table', TemplateView.as_view(template_name='tmp/table.html'), name='table'),
    path('tmp/sse', TemplateView.as_view(template_name='tmp/sse.html'), name='table'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('sse/', sse_view, name='sse'),
]
