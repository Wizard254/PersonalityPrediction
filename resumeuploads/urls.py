from django.urls import path

from resumeuploads.views import JobDescriptionSearch

urlpatterns = [
    path('jds', JobDescriptionSearch.as_view())
]
