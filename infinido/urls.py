from django.contrib import admin
from django.urls import path

from app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("start_over", start_over),
    path("delete", delete),
    path("done", done),
]
