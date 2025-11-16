from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.user_logout, name='logout'),
    path('Student-login', views.studentlogin, name='studentlogin'), #student login
    path('dashboard', views.db, name='exam_user'),                              #student dashboard
    # path('Student-exam', views.student_exam, name='student_exam'), #student exam
    path('available-exam', views.student_available_exam, name='available_exam'), #available exam
    path('take-exam/<int:exam_id>', views.take_exam, name='take-exam'), #take exam
    path('start-exam/<int:exam_id>', views.start_exam, name='start-exam'), #start exam
    path('calculate-marks', views.calculate_marks, name='calculate-marks'),
    path('success', views.success, name='success'),
    
    
    path('admin-login', views.adminlogin, name='adminlogin'),                        #login for admin
    path('admin-view-teacter', views.view_teacher, name='view_teachers'), #view teacher from admin
    path('admin-db', views.admin, name='admin_db'),     #admin dashboard


    path('admin-exam', views.admin_course, name='admin_exam'),          # course form admin
    path('admin-students', views.admin_student, name='admin_student'),          # student form admin
    path('admin-view-students', views.admin_viewstudent, name='admin_viewstudent'), # view student form admin
    path('admin-teacher', views.admin_teacher, name='admin_teacher'),               # teacher form admin

    path('admin-questions', views.admin_question, name='admin_question'), # questions form admin

    path('admin-add-question/<int:id>', views.admin_add_question,name='admin-add-question'), 
    path('admin-upload-question/<int:exam_id>', views.upload_questions_view, name='admin-upload-question'),
    path('admin-create-exams', views.admin_create_exams, name='admin_create_exams'),

    path('admin-view-question/<int:exam_id>', views.admin_view_question, name='admin-view-question'),
    path('admin-view-exam', views.admin_view_exam, name='admin-view-exam'),
    
    path('update-student/<int:student_id>', views.update_student, name='update-student'),
    path('delete-student/<int:student_id>', views.admin_delete_student, name='admin-delete-student'),



    path('admin-delete-exams/<int:id>', views.admin_delete_exam, name='delete-exams'),
    # path('admin-add-question/<int:id>', views.admin_add_question, name='admin_add_question'),
    path('add-question/<int:exam_id>', views.add_question,name='add-question'), 
  


    
]