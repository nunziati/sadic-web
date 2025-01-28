from django.db import models

class PDBInput(models.Model):
    pdb_code = models.CharField(max_length=10, blank=True, null=True)
    pdb_file = models.FileField(upload_to='pdb_files/', blank=True, null=True)

    def __str__(self):
        return self.pdb_code or "PDB File"
