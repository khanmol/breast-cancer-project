from django.db import models
from django.contrib.auth.models import AbstractUser, User

class Prediction(models.Model):
    radius = models.FloatField()
    texture = models.FloatField()
    perimeter = models.FloatField()
    area = models.FloatField()
    smoothness = models.FloatField()
    compactness = models.FloatField()
    concavity = models.FloatField()
    concave_points = models.FloatField()
    symmetry = models.FloatField()
    fractal_dimension = models.FloatField()
    result = models.IntegerField()

    def __str__(self):
        return f"Prediction {self.id}"

# Quiz Model 
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()  # Duration in minutes

    def __str__(self):
        return self.title

# Question Model:
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    options = models.TextField()  # Store options as a comma-separated string
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

#User Response
class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s response to {self.question.question_text}"


