from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='home_page'),
    path('results', views.result, name='result'),
    path('login/', views.login_p, name='login'),
    path('home/', views.dbd, name='home'),
    path('logout/', views.user_logout, name='logout_s'),
    path('logout_t/', views.t_logout, name='logout_t'),
    path('login1/', views.login_t, name='login_t'),
    path('t_dbd/', views.t_dbd, name='teacher_db'),
    path('update_student/<int:student_id>/', views.update_student, name='update_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('delete_result/<int:student_id>/<int:result_id>/', views.delete_result, name='delete_result'),
    path('update_result/<int:student_id>/<int:result_id>/', views.update_result, name='update_result'),

    path('add_student/', views.add_student, name='add_stu'),
    path('bulk_upload/', views.bulk_upload_students, name='bulk_upload'),
]
