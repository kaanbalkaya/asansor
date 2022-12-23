from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name="appmain"

urlpatterns = [
    path('', views.index),
    path('asansor/', views.index),
    path('asansor/index/',views.index,name='index'),
    path('asansor/login/',views.login_wrapper,name='login'),
    path('asansor/logout/',views.logout_wrapper,name='logout'),
    path('asansor/addelevator/',views.addelevator,name='addelevator'),
    path('asansor/adddocument/',views.adddocument,name='adddocument'),
    path("asansor/elevator_detail/<str:id>/",views.elevator_detail, name="elevator_detail"),
    path("asansor/document_detail/<str:id>/",views.document_detail, name="document_detail"),
    path("asansor/success/",views.success,name="success"),
    path("asansor/error/",views.error,name="error"),
    path("asansor/report/",views.report,name="report"),
    
]
