import os
import time
import threading
import uuid
import textwrap
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import PDBInputForm
from datetime import datetime
import sadic

RANGE_RISOLUZIONE = (0.1, 3.0)
RANGE_PROBE_RADIUS = (1.0, 100.0)

# Variabile globale per tracciare lo stato di avanzamento
progress = {}

def get_progress(request):
    """API per restituire lo stato di avanzamento della progress bar"""
    task_id = request.GET.get('task_id', None)
    if not task_id:
        return JsonResponse({"error": "Missing task_id"}, status=400)

    if task_id not in progress:
        return JsonResponse({"error": "Task not found"}, status=404)

    # Se il processo ha fallito, restituisci un messaggio di errore
    if progress[task_id] == -1:
        return JsonResponse({"error": "Processing failed due to an internal error."}, status=500)

    return JsonResponse({"progress": progress[task_id]})


def process_pdb(input_arg, output_path, risoluzione=None, probe_radius=None, task_id=None):
    """Elabora il file e aggiorna il progresso."""
    global progress
    progress[task_id] = 0  # Inizializza il progresso

    def update_progress(percent):
        progress[task_id] = percent

    try:
        update_progress(10)  # Inizio elaborazione
        time.sleep(1)  # Simulazione di operazione lunga
        
        # Controlliamo che l'input sia valido prima di procedere
        if not input_arg:
            raise ValueError("Input argument is missing or invalid.")

        result = sadic.sadic(input_arg, resolution=risoluzione, probe_radius=probe_radius)
        update_progress(50)  # Metà processo
        time.sleep(1)

        if not result:
            raise ValueError("SADIC processing failed. No result returned.")

        result.save_pdb(output_path)
        update_progress(100)  # Completato

    except Exception as e:
        print(f"Error in process_pdb: {e}")
        progress[task_id] = -1  # Indica errore



def cleanup_old_files(directory, days_old):
    """Elimina i file più vecchi di un certo numero di giorni"""
    now = time.time()
    cutoff = now - (days_old * 86400)

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.getmtime(file_path) < cutoff:
                os.remove(file_path)
                print(f"Deleted {file_path}")


def upload_pdb(request):
    """Gestisce l'upload e avvia l'elaborazione in un thread separato."""
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
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            task_id = str(uuid.uuid4())  # Genera un task_id unico

            # Creiamo una cartella per i file di output
            output_dir = os.path.join(settings.MEDIA_ROOT, 'output_files')
            os.makedirs(output_dir, exist_ok=True)

            if not pdb_input.pdb_file and not pdb_input.pdb_code:
                return JsonResponse({"error": "You must provide either a PDB file or a PDB code."}, status=400)

            if pdb_input.pdb_file:
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
                risoluzione = max(RANGE_RISOLUZIONE[0], min(float(risoluzione), RANGE_RISOLUZIONE[1]))

            if probe_radius is not None:
                probe_radius = max(RANGE_PROBE_RADIUS[0], min(float(probe_radius), RANGE_PROBE_RADIUS[1]))

            # Avvia il processo di elaborazione in un thread separato
            thread = threading.Thread(target=process_pdb, args=(input_arg, output_path, risoluzione, probe_radius, task_id))
            thread.start()

            return JsonResponse({"task_id": task_id, "download_url": f"/media/output_files/{output_filename}"})
    
    else:
        form = PDBInputForm()


    titolo = "SADICv2 Web: Simple Atom Depth Index Calculator"
    descrizione = textwrap.dedent("""\
        SADIC v2 is an advanced tool for calculating the depth index of atoms in protein molecules.  
        This web application allows users to either directly input the PDB code of a protein or upload a PDB file.  
        The computed atom depth indices are stored in the B-factor field of the resulting modified PDB file.  

        This solution provides a fast and efficient approach for:
        - 🔬 Assessing atomic depth for structural insights
        - 🧬 Understanding protein stability and molecular interactions.
    """)

    return render(request, 'sadicapp/upload_pdb.html', {'form': form, 'titolo_software': titolo, 'descrizione_software': descrizione})