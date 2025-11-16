import random
from django.shortcuts import render, redirect,get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from resultapp import models
from . import models as mdb_models
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect


from docx import Document
import re
from .utils import import_questions_from_docx
from django import forms
from .models import Exam, Question

from django.utils import timezone
from django.db.models import Q


# Create your views here.

def index(request):
    n = models.Student.objects.all()
    m = models.Student_Result.objects.all()
    o = models.Class.objects.filter(name='Jss1a')
    # t = Teacher.objects.filter()
    return render(request, 'exams/index.html', context={'n': n,'m': m,'o':o})

def studentlogin(request):
     if 'logged_in_user' in request.session:
          return redirect('home')
     elif 'logged_in_teacher' in request.session:
          return redirect('teacher_db')
     else:
          if request.method == 'POST':
               try:
                    admission_num = request.POST['admission_num']
                    password = request.POST['password']
               except Exception:
                    return render(request, 'exams/studentlogin.html', {'error': "Admission Number is not a character"})
               if not admission_num or not password:
                    return render(request, 'exams/studentlogin.html', {'error': "Admission Number and Password IS REQUIRED"})
               else:
                    pass
               try:
                    user = models.Student.objects.get(admission_number=admission_num)
               except models.Student.DoesNotExist:
                    return render(request, 'exams/studentlogin.html', {'error': "Admission Number does not exist"})
                         # Checking if the password matches the password for the username
               if user.password == password:
                    request.session['exam_user'] = admission_num
                    # this will help when the redirecting url has a parameter 'next'
                    new_redirect = request.GET.get('next', 'exam_user')
                    return redirect(new_redirect)
               else:
                    return render(request ,'exams/studentlogin.html', {'error': 'Invalid username or password'})

     return render(request, 'exams/studentlogin.html')
     

def db(request):
    if 'exam_user' in request.session:
        admission_num = request.session['exam_user']
        try:
            user = models.Student.objects.get(admission_number=admission_num)
            result = models.Student_Result.objects.filter(student=user)
            today = timezone.now().date()
            user = models.Student.objects.get(admission_number=admission_num)
            ava_exams = mdb_models.Exam.objects.filter(assigned_class=user.enrolled_class, exam_date=today).count()

            return render(request, 'exams/students/student_dashboard.html', {'result': result, 'user': user, 'ava': ava_exams, })
        except models.Student.DoesNotExist:
            pass
    else:
        return redirect('studentlogin')  # Redirect to the login page if not logge
    
def take_exam(request, exam_id):
     if 'exam_user' in request.session:
        admission_num = request.session['exam_user']
        try:
            user = models.Student.objects.get(admission_number=admission_num)
            today = timezone.now().date()
            exams = mdb_models.Exam.objects.get(id=exam_id)
            question = mdb_models.Question.objects.filter(exams=exams)
            total_q = mdb_models.Question.objects.filter(exams=exams).count()
            return render(request, 'exams/students/take_exam.html', {'user': user, 'exams': exams, 'total_question':total_q })
        except models.Student.DoesNotExist:
            pass

        return render(request, 'exams/students/student_exam.html', {'user':admission_num})
     else:
        return redirect('studentlogin')

def student_available_exam(request):
    if 'exam_user' in request.session:
        admission_num = request.session['exam_user']
        today = timezone.now().date()
        user = models.Student.objects.get(admission_number=admission_num)

        # Get the class name string from the related Class model
        enrolled_class = user.enrolled_class.name  # e.g., 'Jss1a'
        level_prefix = enrolled_class[:-1]         # e.g., 'Jss1'

        # Filter exams for the level (e.g., all 'Jss1' classes)
        ava_exams = mdb_models.Exam.objects.filter(
            assigned_class__istartswith=level_prefix,
            exam_date=today
        )

        if request.method == 'POST':
            code = request.POST.get('code')
            exam_id = request.POST.get('exam_id')
            exam = mdb_models.Exam.objects.get(id=exam_id)
            try:
               if int(code) == exam.code:
                    return redirect('take-exam', exam_id=exam_id)
               else:
                    return render(request, 'exams/students/student_exam.html', {
                         'user': user,
                         'ava': ava_exams,
                         'error': "Invalid Code"
                    })
            except ValueError:
               return render(request, 'exams/students/student_exam.html', {
                    'user': user,
                    'ava': ava_exams,
                    'error': "Code must be a number"
               })

        
        return render(request, 'exams/students/student_exam.html', {'user': user,'ava': ava_exams,})
    else:
        return redirect('studentlogin')
     

def user_logout(request):
    if 'exam_user' in request.session:
        del request.session['exam_user']
    return redirect('index')



def start_exam(request, exam_id):
    if 'exam_user' not in request.session:
        return redirect('studentlogin')

    admission_num = request.session['exam_user']
    try:
        user = models.Student.objects.get(admission_number=admission_num)
        exam = mdb_models.Exam.objects.get(id=exam_id)
        questions = mdb_models.Question.objects.filter(exams=exam)

        if models.Student_Result.objects.filter(student=user, subject=exam).exists():
            return render(request, 'exams/students/start_exam.html', {
                'error': "This exam has already been taken.",
                'user': user,
                'exam': exam,
                'question': [],
                'option_labels': [('option1', 'A'), ('option2', 'B'), ('option3', 'C'), ('option4', 'D')]
            })

        return render(request, 'exams/students/start_exam.html', {
            'question': questions,
            'user': user,
            'exam': exam,
            'option_labels': [('option1', 'A'), ('option2', 'B'), ('option3', 'C'), ('option4', 'D')]
        })

    except (models.Student.DoesNotExist, mdb_models.Exam.DoesNotExist):
        return render(request, 'exams/students/start_exam.html', {
            'error': "Invalid student or exam.",
            'question': [],
            'user': None,
            'exam': None,
            'option_labels': [('option1', 'A'), ('option2', 'B'), ('option3', 'C'), ('option4', 'D')]
        })

# def start_exam(request, exam_id):
#     if 'exam_user' in request.session:
#         admission_num = request.session['exam_user']
#         try:
#             user = models.Student.objects.get(admission_number=admission_num)
#             exam = mdb_models.Exam.objects.get(id=exam_id)

#             questions = mdb_models.Question.objects.filter(exams=exam)

#             if models.Student_Result.objects.filter(student=user, subject=exam).exists():
#                 return render(request, 'exams/students/start_exam.html', {'error': "This Exams Has been taken.", 'user': user})

#         except Exception:
#             pass
#         return render(request, 'exams/students/start_exam.html', {'question': questions, 'user': user, 'exam': exam})
#     else:
#           return redirect('studentlogin')


def calculate_marks(request):
    if 'exam_user' not in request.session:
        return redirect('studentlogin')

    admission_num = request.session['exam_user']
    try:
        user = models.Student.objects.get(admission_number=admission_num)
    except models.Student.DoesNotExist:
        return redirect('studentlogin')

    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        try:
            exam = mdb_models.Exam.objects.get(id=exam_id)
        except mdb_models.Exam.DoesNotExist:
            return redirect('available_exam')

        # Prevent duplicate submissions
        if models.Student_Result.objects.filter(student=user, subject=exam).exists():
            return render(request, 'exams/students/start_exam.html', {
                'error': "You have already taken this exam.",
                'user': user,
                'exam': exam,
                'question': [],
                'option_labels': [('option1', 'A'), ('option2', 'B'), ('option3', 'C'), ('option4', 'D')]
            })

        questions = mdb_models.Question.objects.filter(exams=exam)
        total_marks = sum(q.marks for q in questions)
        obtained_marks = 0

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.answer:
                obtained_marks += question.marks

        # Save result
        models.Student_Result.objects.create(
            student=user,
            subject=exam,
            exam_scores=obtained_marks
        )

        return render(request, 'exams/students/success.html', {
            'user': user,
            'exam': exam,
            'total_marks': total_marks,
            'obtained_marks': obtained_marks
        })

    return HttpResponseRedirect(reverse('student:take_test', args=[exam_id]))


def success(request):
     if 'exam_user' in request.session:
          admission_num = request.session['exam_user']
          user = models.Student.objects.get(admission_number=admission_num)
          
          return render(request, 'exams/students/success.html', {'user': user, })
     else:
          return redirect('studentlogin')










def adminlogin(request):
    if 'logged_in_user' in request.session:
        return redirect('home')
    elif 'logged_in_teacher' in request.session:
          return redirect('teacher_db')
    else:
          if request.method == 'POST':
               try:
                    username = request.POST['username']
                    password = request.POST['password']
               except Exception:
                    return render(request, 'exams/admin/adminlogin.html', {'error': "Username is not a character"})
               if not username or not password:
                    return render(request, 'exams/admin/adminlogin.html', {'error': "Username and Password IS REQUIRED"})
               else:
                    pass
               try:
                    user = mdb_models.AdminUser.objects.get(username=username)
               except mdb_models.AdminUser.DoesNotExist:
                    return render(request, 'exams/admin/adminlogin.html', {'error': "Admission Number does not exist"})
                    # Checking if the password matches the password for the username
               if user.password == password:
                    request.session['admin_user'] = username
                    # this will help when the redirecting url has a parameter 'next'
                    new_redirect = request.GET.get('next', 'admin_db')
                    return redirect(new_redirect)
               else:
                    return render(request ,'exams/admin/adminlogin.html', {'error': 'Invalid username or password'})

          return render(request, 'exams/admin/adminlogin.html')
    

def admin(request):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          total_students = models.Student.objects.all().count()
          total_teacher = models.Teacher.objects.all().count()
          return render(request, 'exams/admin/admin_dashboard.html', context={'total_students': total_students, 'user': AdminUser, 'total_teacher': total_teacher})
     else:
          return redirect('adminlogin')

def view_teacher(request):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          teachers = models.Teacher.objects.all()
          return render(request, 'exams/admin/admin_view_teacher.html', context={'teachers': teachers,'user': AdminUser})
     return redirect('adminlogin')

def admin_course(request):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          return render(request, 'exams/admin/admin_exam.html', context={'user': AdminUser})
     

def admin_student(request):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          x = models.Student.objects.all().count()

          return render(request, 'exams/admin/admin_student.html', context={'x':x, 'user': AdminUser})

def update_student(request, student_id):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          student = models.Student.objects.get(id=student_id)
          classes = models.Class.objects.all()

          if request.method == 'POST':
               name = request.POST.get('name')
               username = request.POST.get('username')
               password = request.POST.get('password')
               admission_number = request.POST.get('admission_number')
               address = request.POST.get('address')
               enrolled_class = request.POST.get('class')
               year = request.POST.get('year')
               month = request.POST.get('month')
               day = request.POST.get('day')
               if IntegrityError:
                    return render(request, 'exams/admin/update_student.html', context={'user': AdminUser, 'student': student, 'classes': classes, 'error': "Details Exists Already"})
               
               DOB = 'year' + '-' + 'month' + '-' + 'day'
              

               new_student = models.Student(name=name, 
                                             username=username, 
                                             password=password, 
                                             admission_number=admission_number, 
                                             address=address,
                                             enrolled_class=student.enrolled_class,
                                                  DOB=DOB, 
                                             )

               new_student.save()
              
          return render(request, 'exams/admin/update_student.html', context={'user': AdminUser, 'student': student, 'classes': classes})

def admin_viewstudent(request):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          x = models.Student.objects.all()
          classes = models.Class.objects.all()

          return render(request, 'exams/admin/admin_view_student.html', context={'x':x,'classes': classes,'user': AdminUser})


def admin_teacher(request):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          x = models.Teacher.objects.all().count()

          return render(request, 'exams/admin/admin_teacher.html', context={'x':x,'user': AdminUser})



def admin_question(request):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          

          return render(request, 'exams/admin/admin_question.html', context={'user': AdminUser})


def admin_create_exams(request):
    if 'admin_user' in request.session:
        AdminUser = request.session['admin_user']
        classes = models.Class.objects.all()

        if request.method == 'POST':
            subj = request.POST.get('SubjectName')
            day = request.POST.get('day')
            month = request.POST.get('month')
            year = request.POST.get('year')
            exams_class = request.POST.get('class')

            subj1 = subj.capitalize()
            if mdb_models.Exam.objects.filter(subj_name=subj1, assigned_class=exams_class).exists():
                return render(request, 'exams/admin/admin_create_exam.html', context={
                    'error': 'This exam already exists for this class!!',
                    'n': classes,
                    'user': AdminUser
                })

            Examdate = f"{year}-{month}-{day}"

            # Generate a unique 4-digit code
            while True:
                exam_code = random.randint(1000, 9999)
                if not mdb_models.Exam.objects.filter(code=exam_code).exists():
                    break

            # Create the exam with the unique code
            mdb_models.Exam.objects.create(
                assigned_class=exams_class,
                subj_name=subj1,
                exam_date=Examdate,
                code=exam_code
            )

            return redirect('admin-view-exam')

        return render(request, 'exams/admin/admin_create_exam.html', context={'user': AdminUser, 'n': classes})
def admin_view_question(request, exam_id):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          exam = mdb_models.Exam.objects.get(id=exam_id)
          x = mdb_models.Question.objects.filter(exams=exam)

          return render(request, 'exams/admin/view_question.html', context={'exam': exam, 'x':x, 'user': AdminUser})
     
def admin_view_exam(request):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          x = mdb_models.Exam.objects.all()

          return render(request, 'exams/admin/admin_view_exam.html', context={'x':x,'user': AdminUser})
     

def admin_delete_exam(request, id):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          exam = mdb_models.Exam.objects.get(id=id)
          exam.delete()
          return redirect('admin-view-exam')

     return redirect('adminlogin')

def admin_delete_student(request, student_id):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          studt = models.Student.objects.get(id=student_id)
          studt.delete()
          return redirect('admin_viewstudent')

     return redirect('adminlogin')

def admin_add_question(request, exam_id):
     if 'admin_user' in request.session:
          AdminUser = request.session['admin_user']
          exam = mdb_models.Exam.get(id=exam_id)
          if request.method == 'POST':
               
               question = request.POST.get('question')
               mark = request.POST.get('marks')
               op1 = request.POST.get('op1')
               op2 = request.POST.get('op2')
               op3 = request.POST.get('op3')
               op4 = request.POST.get('op4')
               answer = request.POST.get('answer')
               

               new_question = mdb_models.Question(
                    exam=exam.subj_name,
                    question=question,
                    option1=op1,
                    option2=op2,
                    option3=op3,
                    option4=op4,
                    answer=answer,
                    marks=mark
                    )

               new_question.save()
          return render(request, 'exams/admin/admin_add_question.html' , context={'user': AdminUser,'exam':exam})
     return redirect('adminlogin')

def upload_questions_view(request, exam_id):
    try:
        exam = mdb_models.Exam.objects.get(id=exam_id)
        AdminUser = request.session['admin_user']
    except mdb_models.Exam.DoesNotExist:
        raise Http404("Exam does not exist")
    except KeyError:
        return HttpResponse("Unauthorized: Admin session not found", status=401)

    if request.method == 'POST':
        uploaded_file = request.FILES.get('docx_file')
        if uploaded_file and uploaded_file.name.endswith('.docx'):
            import_questions_from_docx(uploaded_file, exam)
            return redirect('admin-view-question', exam_id)
        else:
          return render(request, 'exams/admin/admin_add_question.html', {'error': "Invalid file format. Please upload a .docx file.", 'user': AdminUser, 'exam':exam})
    return render(request,  'exams/admin/admin_add_question.html' , context={'user': AdminUser,'exam':exam})

def add_question(request, exam_id):
    try:
        exam = mdb_models.Exam.objects.get(id=exam_id)
        
        AdminUser = request.session['admin_user']
    except mdb_models.Exam.DoesNotExist:
        raise Http404("Exam does not exist")


    return render(request,  'exams/admin/admin_add_question.html' , context={'user': AdminUser,'exam':exam})



