import os
import sys
import json
import django

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Licenciatura, UnidadeCurricular, Docente

def import_data():
    course_file = 'files/ULHT260-PT.json'
    
    if not os.path.exists(course_file):
        print(f"Erro: Ficheiro {course_file} não encontrado.")
        return

    with open(course_file, 'r', encoding='utf-8') as f:
        course_data = json.load(f)

    # 1. Import Licenciatura
    licenciatura, created = Licenciatura.objects.get_or_create(
        nome="Engenharia Informática",
        defaults={
            'apresentacao': "Curso de Engenharia Informática da Universidade Lusófona.",
            'objetivos': "Formar profissionais qualificados na área de TI...",
            'competencias': "Desenvolvimento de software, redes, sistemas...",
            'saidas_profissionais': "Software Engineer, Systems Admin, etc.",
            'razoes_escolha': "\n".join([r['reason'] for r in course_data.get('reasons', [])])
        }
    )
    if created:
        print(f"Criada Licenciatura: {licenciatura}")
    else:
        # Atualizar razões de escolha se já existir
        licenciatura.razoes_escolha = "\n".join([r['reason'] for r in course_data.get('reasons', [])])
        licenciatura.save()
        print(f"Atualizada Licenciatura: {licenciatura}")

    # 2. Import UCs
    for uc_data in course_data.get('courseFlatPlan', []):
        uc_code = uc_data['curricularIUnitReadableCode']
        uc_detail_file = f'files/{uc_code}-PT.json'
        
        detail = {}
        if os.path.exists(uc_detail_file):
            with open(uc_detail_file, 'r', encoding='utf-8') as f:
                detail = json.load(f)

        uc_obj, created = UnidadeCurricular.objects.update_or_create(
            sigla=uc_code.split('-')[-1],
            licenciatura=licenciatura,
            defaults={
                'nome': uc_data['curricularUnitName'],
                'ano': uc_data['curricularYear'],
                'semestre': 1 if uc_data['semesterCode'] == 'S' else 2,
                'creditos': uc_data['ects'],
                'objetivos': detail.get('objectives', ''),
                'conteudos': detail.get('programme', ''),
                'metodologia': detail.get('methodology', ''),
                'bibliografia': detail.get('bibliography', ''),
                'natureza': detail.get('nature', ''),
                'avaliacao': detail.get('avaliacao', ''),
            }
        )
        print(f"{'Criada' if created else 'Atualizada'} UC: {uc_obj}")

if __name__ == '__main__':
    import_data()
