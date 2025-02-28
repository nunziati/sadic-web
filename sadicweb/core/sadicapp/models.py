from django.db import models

class PDBInput(models.Model):
    pdb_code = models.CharField(max_length=10, blank=True, null=True)
    pdb_file = models.FileField(upload_to='pdb_files/', blank=True, null=True)

    class Meta:
        app_label = 'sadicapp'  # Assicurati che sia il nome dell'app corretta    

    def __str__(self):
        return self.pdb_code or "PDB File"
