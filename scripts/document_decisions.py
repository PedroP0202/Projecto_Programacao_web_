import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import MakingOf

def document():
    MakingOf.objects.create(
        titulo="Decisões de Modelação e Importação de Dados",
        descricao="Documentação das decisões tomadas durante a importação de dados da API Lusófona e JSON de TFCs.",
        decisoes_tomadas="""
1. Adição de campos detalhados às Unidades Curriculares: Foram adicionados campos de 'natureza' e 'avaliacao' para acomodar os dados ricos fornecidos pela API da Lusófona.
2. Relacionamento ManyToMany para Docentes: Mantido para permitir que várias UCs partilhem os mesmos docentes.
3. Importação via ORM: Criados scripts de importação ('loader_lusofona.py' e 'loader_tfcs.py') que garantem a integridade referencial dos dados.
4. TFCs: Criado um ficheiro JSON de exemplo para 2025 para demonstrar a funcionalidade de importação.
        """,
        erros_e_correcoes="""
- Problema com sys.path nos scripts: Corrigido adicionando o diretório atual ao path para que o Django encontre o módulo 'config'.
- Sincronização de migrações: Foram integradas as migrations 0002 e 0003 para garantir que todos os campos estão na base de dados.
        """,
        uso_ia="A IA foi utilizada para gerar os scripts de importação e mapear os campos da API JSON para os modelos Django de forma eficiente."
    )
    print("Decisões documentadas no Making Of com sucesso.")

if __name__ == '__main__':
    document()
