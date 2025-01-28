from django import forms
from .models import PDBInput

class PDBInputForm(forms.ModelForm):
    class Meta:
        model = PDBInput
        fields = ['pdb_code', 'pdb_file']
        widgets = {
            'pdb_code': forms.TextInput(attrs={'placeholder': 'Inserisci codice PDB'}),
        }
