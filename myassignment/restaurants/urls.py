from django.contrib import admin
from django.urls import path, include
from .urls import *
from .views import *

urlpatterns = [path("", index, name="index")]
