from django import forms


class BreastCancerPredictionForm(forms.Form):
    radius = forms.FloatField(label='Radius')
    texture = forms.FloatField(label='Texture')
    perimeter = forms.FloatField(label='Perimeter')
    area = forms.FloatField(label='Area')
    smoothness = forms.FloatField(label='Smoothness')
    compactness = forms.FloatField(label='Compactness')
    concavity = forms.FloatField(label='Concavity')
    concave_points = forms.FloatField(label='Concave Points')
    symmetry = forms.FloatField(label='Symmetry')
    fractal_dimension = forms.FloatField(label='Fractal Dimension')
