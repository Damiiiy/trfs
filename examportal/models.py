from django.db import models


# Create your models here.


class AdminUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class Exam(models.Model):
     assigned_class = models.CharField(max_length=100)
     subj_name = models.CharField(max_length=100, null=True)
     exam_date = models.DateField()
     code = models.IntegerField( null=True, blank=True, default=0000)
    
    
     def __str__(self):
        return self.subj_name



class Question(models.Model):
    exams = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks = models.IntegerField( default=1)
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat=(('A','A'),
         ('B','B'),
         ('C','C'),
         ('D','D'))
    answer=models.CharField(max_length=200,choices=cat)

    def __str__(self):
        return f"{self.exams} ({self.exams.assigned_class}) ({self.exams.exam_date}) ({self.exams.subj_name}) ({self.answer})"


class MCQ(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks = models.IntegerField(default=1)
    question_text = models.TextField( default=1)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1)  # 'A', 'B', 'C', or 'D'
    topic = models.CharField(max_length=255, blank=True)