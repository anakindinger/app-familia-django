from django import forms
from dashboard.models import Child

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'dn', 'height', 'weight']

    def clean(self):
        cleaned_data = super().clean()
        # Adicione validações extras se necessário
        return cleaned_data
