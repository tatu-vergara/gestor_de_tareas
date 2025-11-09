
from django import forms

class TareaForm(forms.Form):
    titulo = forms.CharField(
        label="Título",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej.: Llamar a..."}),
    )
    descripcion = forms.CharField(
        label="Descripción",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Detalles de la tarea"}),
    )
