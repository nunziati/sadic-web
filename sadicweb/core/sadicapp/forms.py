from django import forms
from .models import PDBInput

class PDBInputForm(forms.ModelForm):
    risoluzione = forms.DecimalField(
        required=False,
        min_value=0.1,
        max_value=1.5,
        decimal_places=2,
        max_digits=3,
        label='Risoluzione'
    )
    probe_radius = forms.DecimalField(
        required=False,
        min_value=1.0,
        max_value=100.0,
        decimal_places=2,
        max_digits=5,
        label='Probe Radius'
    )

    class Meta:
        model = PDBInput
        fields = ['pdb_file', 'pdb_code', 'risoluzione', 'probe_radius']
        widgets = {
            'pdb_code': forms.TextInput(attrs={'placeholder': 'Inserisci codice PDB'}),
        }
