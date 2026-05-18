# Projecto Programacao Web

Portfolio academico em Django, com apps para portfolio, artigos, contas e escola online. O projeto esta preparado para desenvolvimento local e deploy na Vercel.

## Funcionalidades

- Portfolio com licenciatura, unidades curriculares, projetos, tecnologias, competencias, formacoes, interesses, TFCs e making of.
- Area de gestao protegida por grupo/permissoes.
- Suporte a `DATABASE_URL` para Postgres em producao.
- Seed automatico dos dados principais do portfolio.
- Criacao automatica de superuser por variaveis de ambiente.
- Suporte opcional a Cloudinary para uploads persistentes de media.

## Estrutura

```text
accounts/        autenticacao, grupos e permissoes
artigos/         gestao e visualizacao de artigos
config/          settings, urls, ASGI e WSGI
data/            dados de apoio
escola_online/   paginas da area escola
files/           ficheiros JSON importados da Lusofona
portfolio/       app principal do portfolio
scripts/         scripts de importacao e apoio
```

## Desenvolvimento local

1. Criar e ativar ambiente virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Criar o ficheiro `.env` a partir de `.env.example` e ajustar os valores.
4. Aplicar migracoes e carregar dados:

```bash
python manage.py migrate
python manage.py seed_portfolio
python manage.py ensure_portfolio_manager
```

5. Arrancar o servidor:

```bash
python manage.py runserver
```

## Variaveis de ambiente

As principais variaveis estao documentadas em `.env.example`.

- `DJANGO_SECRET_KEY`: chave secreta da aplicacao.
- `DJANGO_DEBUG`: usar `False` em producao.
- `ALLOWED_HOSTS`: dominios permitidos, separados por virgula.
- `CSRF_TRUSTED_ORIGINS`: origens HTTPS confiaveis, separadas por virgula.
- `DATABASE_URL`: URL da base de dados de producao.
- `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`, `DJANGO_SUPERUSER_EMAIL`: credenciais do admin criado no deploy.
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`: ativam Cloudinary quando as tres estiverem definidas.

## Deploy na Vercel

1. Fazer `push` do repositorio para o GitHub.
2. Importar o repositorio na Vercel.
3. Adicionar uma base de dados Postgres em `Storage`.
4. Configurar as variaveis de ambiente com base em `.env.example`.
5. Fazer o deploy.

O build esta configurado em `pyproject.toml` para aplicar migracoes, carregar dados iniciais, criar/atualizar o superuser, garantir o grupo de gestores e recolher ficheiros estaticos.

## Media e imagens

Em desenvolvimento, os uploads usam a pasta local `media/`. Em producao, a Vercel nao garante persistencia para uploads locais; para imagens persistentes, configura Cloudinary nas variaveis de ambiente.
