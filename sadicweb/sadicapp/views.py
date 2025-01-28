import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PDBInputForm
from .models import PDBInput

def handle_uploaded_file(file):
    with open('uploaded_file.pdb', 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

def process_pdb_file(input_path, output_path):
    # Qui chiami il tuo programma Python
    # Supponiamo che sia un file chiamato `process.py` con una funzione `run(input, output)`
    import subprocess
    subprocess.run(['sadic', input_path, '--output', output_path])

def upload_pdb(request):
    if request.method == 'POST':
        form = PDBInputForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva i dati
            pdb_input = form.save()
            
            # Controlla l'input e salva il file per elaborazione
            input_path = None
            if pdb_input.pdb_file:
                handle_uploaded_file(pdb_input.pdb_file)
                input_path = 'uploaded_file.pdb'
            elif pdb_input.pdb_code:
                # Scarica il file PDB da un repository online basato sul codice
                input_path = f'{pdb_input.pdb_code}.pdb'
                with open(input_path, 'w') as f:
                    f.write("PDB Content Placeholder")  # Qui dovresti scaricare il vero file PDB

            # Elabora il file
            output_path = 'output_file.pdb'
            process_pdb_file(input_path, output_path)

            # Fornisci il file per il download
            with open(output_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_path)}"'
                return response
    else:
        form = PDBInputForm()
    return render(request, 'sadicapp/upload_pdb.html', {'form': form})
