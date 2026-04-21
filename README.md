# Projecto Programacao Web

Projeto Django preparado para deploy na Vercel com:

- suporte a `DATABASE_URL` para Postgres em produção
- seed automático dos dados principais do portfólio
- criação automática de superuser via variáveis de ambiente
- `collectstatic` no build para o admin funcionar corretamente

## Deploy na Vercel

1. Fazer `push` do repositório para o GitHub.
2. Importar o repositório na Vercel.
3. Na Vercel, adicionar uma base de dados Postgres em `Storage`.
4. Definir as variáveis de ambiente com base em `.env.example`.
5. Fazer o deploy.

O build está configurado em `pyproject.toml` para:

- aplicar migrações
- carregar os dados iniciais
- criar/atualizar o superuser
- recolher ficheiros estáticos

## Credenciais de admin

As credenciais do admin no deploy são controladas por:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_PASSWORD`
- `DJANGO_SUPERUSER_EMAIL`

## Nota sobre imagens

O projeto fica pronto para deploy e navegação/admin. No entanto, uploads persistentes de media na Vercel exigem storage adicional; sem isso, não deves depender de uploads novos como parte central da avaliação.

Para evitar conflitos com variáveis globais do sistema, usa `DJANGO_DEBUG=False` em produção em vez de depender de `DEBUG`.
