
from django.contrib import admin
from django.urls import path
from . import views 
from school.models import Grade

urlpatterns = [

    path('', views.index,  name="home"),
    path('classe/create/', views.create_class, name="create-class"),
    path('classes/<int:class_id>', views.check_class, name="check-class"), 
    path('classes/', views.classes_list, name="classes"),
    path('classe/eleves/<int:class_id>', views.afficher_eleves, name="liste_eleves"),
    path('courses/create/<int:class_id>', views.create_course, name="create-course"),
    path('courses/<int:course_id>', views.check_course, name="check-course"),
    path('courses/cotes/<int:course_id>', views.afficher_cotes, name="afficher-cotes"),
    path('classe/<int:class_id>/student/<int:student_id>/report/', views.get_student_report, name="student-report"),
]