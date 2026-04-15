import os
import sys
import json
import django

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import TFC

def import_tfcs():
    tfc_file = 'data/tfc_2025.json'
    
    if not os.path.exists(tfc_file):
        print(f"Erro: Ficheiro {tfc_file} não encontrado.")
        return

    with open(tfc_file, 'r', encoding='utf-8') as f:
        tfc_list = json.load(f)

    for tfc_data in tfc_list:
        tfc_obj, created = TFC.objects.get_or_create(
            titulo=tfc_data['titulo'],
            defaults={
                'autores': tfc_data['autores'],
                'orientadores': tfc_data['orientadores'],
                'ano': tfc_data['ano'],
                'resumo': tfc_data['resumo'],
                'destaque': tfc_data['destaque'],
            }
        )
        print(f"{'Criado' if created else 'Já existe'} TFC: {tfc_obj}")

if __name__ == '__main__':
    import_tfcs()
