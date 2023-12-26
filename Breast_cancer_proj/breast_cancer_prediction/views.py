
from django.shortcuts import render, redirect
from .forms import BreastCancerPredictionForm
import joblib
import numpy as np
import os  # Add this line to import the os module
from .models import Prediction
from sklearn.preprocessing import StandardScaler
from .models import Quiz, Question, UserResponse

# Quiz View
def quiz_view(request):
    quiz = Quiz.objects.first()  # Get the first quiz from the database
    questions = Question.objects.filter(quiz=quiz)
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quiz_template.html', context)

# submitting answers
def submit_quiz(request):
    if request.method == 'POST':
        user = request.user  # Assuming you have user authentication implemented
        quiz = Quiz.objects.first()  # Get the first quiz from the database
        questions = Question.objects.filter(quiz=quiz)

        # Iterate over the submitted answers and save them
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            UserResponse.objects.create(user=user, question=question, selected_option=selected_option)

        # Calculate the score
        correct_responses = UserResponse.objects.filter(user=user, question__quiz=quiz, selected_option=F('question__correct_answer'))
        score = (correct_responses.count() / questions.count()) * 100

        return render(request, 'result.html', {'score': score})
    else:
        return redirect('quiz_view')


def quiz_result(request):
    # Retrieve the user's quiz responses and calculate the score
    user_responses = UserResponse.objects.filter(user=request.user)
    total_questions = user_responses.count()
    correct_answers = user_responses.filter(is_correct=True).count()
    score = (correct_answers / total_questions) * 100

    # Render the quiz_result template with the data
    return render(request, 'quiz_result.html', {
        'score': score,
    })
    
def predict_breast_cancer(data):
    # Load the saved model
    model = joblib.load('breast_cancer_model.pkl')
    # Reshape the data to match the model's expectations
    reshaped_data = data.reshape(1, -1)
    # Perform the prediction
    prediction = model.predict(reshaped_data)
    # Return the prediction
    return prediction

def predict(request):
    if request.method == 'POST':
        form = BreastCancerPredictionForm(request.POST)
        if form.is_valid():
            data = []
            for key in form.cleaned_data:
                value = form.cleaned_data[key]
                data.append(value)
            data = np.array(data)  # Convert data to a numpy array
            
            
            # Perform feature scaling
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(data.reshape(1, -1))

            
            result = predict_breast_cancer(data)

            # Save the values in the database
            prediction = Prediction.objects.create(
                radius=data_scaled[0][0],
                texture=data_scaled[0][1],
                perimeter=data_scaled[0][2],
                area=data_scaled[0][3],
                smoothness=data_scaled[0][4],
                compactness=data_scaled[0][5],
                concavity=data_scaled[0][6],
                concave_points=data_scaled[0][7],
                symmetry=data_scaled[0][8],
                fractal_dimension=data_scaled[0][9],
                result=result,
            )

            return render(request, 'result.html', {'result': result})
    else:
        form = BreastCancerPredictionForm()

    return render(request, 'predict.html', {'form': form})
