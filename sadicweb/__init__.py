from __future__ import absolute_import, unicode_literals
import os
import sys


__version__ = '1.0'
VERSION = __version__




def manage():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sadicweb.config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)