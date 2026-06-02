# app-familia-django

## Sobre o Projeto

Este repositório contém uma aplicação Django usada para gerenciar funcionalidades relacionadas a uma família/colegas de cuidado: agendas, chat, painel administrativo e rotinas. A estrutura principal inclui apps como `agenda`, `chat`, `dashboard`, `rotina` e `usuario`, e usa SQLite por padrão (arquivo `db.sqlite3`).

## Como Rodar

Requisitos mínimos:
- Python 3.10+ (ou versão compatível do seu ambiente)

Passos rápidos:

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. (Opcional) Copie variáveis de ambiente do exemplo e ajuste conforme necessário:

```bash
cp .env.example .env
# editar .env conforme necessário
```

4. Rode as migrações:

```bash
python manage.py migrate
```

5. Crie um superusuário (opcional):

```bash
python manage.py createsuperuser
```

6. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O projeto ficará disponível em `http://127.0.0.1:8000/` por padrão.

Se for necessário coletar arquivos estáticos (para produção ou testes específicos):

```bash
python manage.py collectstatic
```


