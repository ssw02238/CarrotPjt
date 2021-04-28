from django.urls import path
from . import views


app_name = 'questions'

urlpatterns = [
    path('', views.indexing, name='indexing'),
    path('write/', views.write, name='write'),
    path('<int:question_pk>/detailing/', views.detailing, name='detailing'),
    path('<int:question_pk>/deleting/', views.deleting, name='deleting'),
    # path('<int:question_pk>/update', views.update, name='update'),
]