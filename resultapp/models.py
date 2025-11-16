from django.db import models
from examportal.models import *

# Create your models here.


class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    assigned_class = models.OneToOneField(Class, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100, unique=True, null=True, )
    password = models.CharField(max_length=20, null=True )

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=20, null=True)
    admission_number = models.CharField(null=True, unique=True)
    address = models.CharField(max_length=100)
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name



class Student_Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Exam, on_delete=models.CASCADE, null=False)
    test_scores = models.IntegerField(default=0, blank=True)
    exam_scores = models.IntegerField(default=0, blank=True)
    total_scores = models.IntegerField( editable=False)

    # object = StudentResultManager()


    @property
    def grade(self):
        if self.total_scores >= 80:
            return 'A1'
        elif self.total_scores >= 75:
            return 'A2'
        elif self.total_scores >= 70:
            return 'A3'
        elif self.total_scores >= 65:
            return 'C4'
        elif self.total_scores >= 60:
            return 'C5'
        elif self.total_scores >= 55:
            return 'C6'
        elif self.total_scores >= 50:
            return 'P7'
        elif self.total_scores >= 45:
            return 'P8'
        else:
            return 'F9'
        
    def save(self, *args, **kwargs):
        self.total_scores = self.test_scores + self.exam_scores  # calculate total_scores
        super().save(*args, **kwargs)  # call the original save method

    def update_test_scores(self, new_test_scores):
        self.test_scores = new_test_scores
        self.total_scores = self.test_scores + self.exam_scores  # Update total_scores
        self.save()  # Save the changes
    def __str__(self):
        return f'{self.student.name}'
    

    