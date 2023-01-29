from django.urls import path
from . import views

urlpatterns = [
    # path('',views.home)
    path('<str:group_name>/',views.home)
]
