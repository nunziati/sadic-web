import os
import time

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PDBInputForm
from datetime import datetime

from sadic import sadic

RANGE_RISOLUZIONE = (0.1, 3.0)
RANGE_PROBE_RADIUS = (1.0, 100.0)

def process_pdb(input, output_path, risoluzione=None, probe_radius=None):
    result = sadic(input, resolution=risoluzione, probe_radius=probe_radius)
    result.save_pdb(output_path)

def cleanup_old_files(directory, days_old):
    now = time.time()
    cutoff = now - (days_old * 86400)

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.getmtime(file_path) < cutoff:
                os.remove(file_path)
                print(f"Deleted {file_path}")

def upload_pdb(request):
    # Esegui la pulizia dei file vecchi
    days_old = 5 / (24 * 60)
    input_dir = os.path.join(settings.MEDIA_ROOT, 'pdb_files')
    output_dir = os.path.join(settings.MEDIA_ROOT, 'output_files')
    cleanup_old_files(input_dir, days_old)
    cleanup_old_files(output_dir, days_old)

    if request.method == 'POST':
        form = PDBInputForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva i dati
            pdb_input = form.save()

            # Genera un timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

            # Creiamo una cartella per i file di output
            output_dir = os.path.join(settings.MEDIA_ROOT, 'output_files')
            os.makedirs(output_dir, exist_ok=True)

            if pdb_input.pdb_file:  # Se l'utente ha caricato un file
                input_arg = pdb_input.pdb_file.path
                input_filename = os.path.basename(input_arg)
                input_filename_with_timestamp = f"{timestamp}_{input_filename}"
                input_arg_with_timestamp = os.path.join(os.path.dirname(input_arg), input_filename_with_timestamp)
                os.rename(input_arg, input_arg_with_timestamp)
                input_arg = input_arg_with_timestamp
                output_filename = input_filename_with_timestamp
            elif pdb_input.pdb_code:  # Se l'utente ha inserito un codice
                input_arg = pdb_input.pdb_code
                output_filename = f'{timestamp}_{input_arg}.pdb'
 
            output_path = os.path.join(output_dir, output_filename)

            # Ottieni i valori di risoluzione e probe_radius
            risoluzione = form.cleaned_data.get('risoluzione')
            probe_radius = form.cleaned_data.get('probe_radius')

            if risoluzione is not None:
                if risoluzione < RANGE_RISOLUZIONE[0]:
                    risoluzione = RANGE_RISOLUZIONE[0]
                elif risoluzione > RANGE_RISOLUZIONE[1]:
                    risoluzione = RANGE_RISOLUZIONE[1]

            if probe_radius is not None:
                if probe_radius < RANGE_PROBE_RADIUS[0]:
                    probe_radius = RANGE_PROBE_RADIUS[0]
                elif probe_radius > RANGE_PROBE_RADIUS[1]:
                    probe_radius = RANGE_PROBE_RADIUS[1]

            # Elabora il file
            process_pdb(input_arg, output_path, risoluzione, probe_radius)

            # Fornisci il file per il download
            with open(output_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
                return response
    else:
        form = PDBInputForm()

    titolo = "SADIC v2: A Modern Implementation of the Simple Atom Depth Index Calculator"
    descrizione = """ SADIC v2 is an advanced tool for calculating the depth index of atoms in protein molecules.  
                    This web application allows users to either directly input the PDB code of a protein or upload a PDB file.  
                    The computed atom depth indices are stored in the B-factor field of the resulting modified PDB file.  
                    This solution provides a fast and efficient approach for assessing atomic depth, enabling accurate structural analyses of proteins.
                """
    
    return render(request, 'sadicapp/upload_pdb.html', {'form': form, 'titolo_software': titolo, 'descrizione_software': descrizione})