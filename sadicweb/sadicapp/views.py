import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PDBInputForm
from .models import PDBInput

def process_pdb(input, output_path):
    import subprocess
    subprocess.run(['sadic', input, "--output", output_path])

def upload_pdb(request):
    if request.method == 'POST':
        form = PDBInputForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva i dati
            pdb_input = form.save()

            # Determina il percorso del file caricato
            input_path = None
            if pdb_input.pdb_file:  # Se l'utente ha caricato un file
                input_path = pdb_input.pdb_file.path
            elif pdb_input.pdb_code:  # Se l'utente ha inserito un codice
                input_path = os.path.join(settings.MEDIA_ROOT, f"{pdb_input.pdb_code}.pdb")
                with open(input_path, 'w') as f:
                    f.write("PDB Content Placeholder")  # Qui scarichi il vero file PDB

            # Creiamo una cartella per i file di output
            output_dir = os.path.join(settings.MEDIA_ROOT, 'output_files')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'output_file.pdb')

            # Elabora il file
            process_pdb_file(input_path, output_path)

            # Fornisci il file per il download
            with open(output_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="output_file.pdb"'
                return response
    else:
        form = PDBInputForm()
    return render(request, 'sadicapp/upload_pdb.html', {'form': form})



def home(request):
    titolo = "SADIC v2: A Modern Implementation of the Simple Atom Depth Index Calculator"
    descrizione = """ SADIC v2 is an advanced tool for calculating the depth index of atoms in protein molecules.  
                    This web application allows users to either directly input the PDB code of a protein or upload a **PDB file**.  
                    The computed atom depth indices are stored in the B-factor field of the resulting modified PDB file.  
                    This solution provides a fast and efficient approach for assessing atomic depth, enabling accurate structural analyses of proteins.
                """
    return render(request, 'home.html', {'titolo_software': titolo, 'descrizione_software': descrizione})


