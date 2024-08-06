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
    cat=(('Option1','Option1'),
         ('Option2','Option2'),
         ('Option3','Option3'),
         ('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

    def __str__(self):
        return f"{self.exams} ({self.exams.assigned_class}) ({self.exams.exam_date}) ({self.exams.subj_name}) ({self.answer})"
