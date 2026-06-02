
# 👨‍👩‍👧‍👦 Família Conectada

Aplicação web desenvolvida com Django para apoiar a organização e a comunicação entre responsáveis, com foco na redução de conflitos, previsibilidade de rotinas e melhoria da convivência familiar.

---

## 📌 Sobre o projeto

O **Família Conectada** nasce a partir de um problema real observado no contexto do sistema de justiça:  
a dificuldade de comunicação entre responsáveis (especialmente em situações de separação), que frequentemente gera conflitos, ruídos de informação e impactos diretos no bem-estar de crianças e adolescentes.

Em muitos casos:
- Há dificuldade na organização de rotinas e responsabilidades
- A comunicação é carregada de conflito ou ambiguidade
- Informações importantes se perdem ou geram mal-entendidos
- Pequenas decisões do dia a dia acabam escalando para disputas maiores

O objetivo da aplicação é oferecer **uma estrutura digital clara, previsível e orientada à mediação**, reduzindo atritos e promovendo interações mais organizadas.

---

## 🎯 Objetivos da solução

- Centralizar informações familiares em um único ambiente
- Facilitar a comunicação entre responsáveis
- Reduzir conflitos por meio de estrutura e previsibilidade
- Oferecer base para mediação assistida por tecnologia
- Criar base para integração com inteligência artificial (IA)

---

## 🧠 Contexto institucional

Este projeto foi desenvolvido no contexto do:

**Tribunal de Justiça do Paraná (TJPR)**  
Laboratório de Inovação

A proposta está alinhada com iniciativas de:
- simplificação da experiência do cidadão
- uso de tecnologia para prevenção de conflitos
- aplicação de inteligência artificial no sistema de justiça

---

## 🏗️ Arquitetura da aplicação

O projeto utiliza o framework Django, seguindo a arquitetura padrão do framework:

### Backend (Django)
- **Models** → estruturação e persistência dos dados
- **Views** → definição da lógica de negócio
- **Templates** → renderização da interface web
- **URLs** → roteamento das requisições

### Persistência de dados
- Banco de dados relacional
- SQLite (ambiente de desenvolvimento)

### Organização
- Aplicações Django modulares
- Separação de responsabilidades por camada

---

## 🚀 Tecnologias utilizadas

- **Python**
- **Django**
- **SQLite**
- HTML / CSS
- Git / GitHub

---

## ⚙️ Funcionalidades (atual)

- Estrutura base de aplicação web com Django
- Modelagem de dados para representação de entidades familiares
- Interface web com templates Django
- Organização de fluxo de interação entre usuários
- Base para evolução com novas funcionalidades

---

## 🔮 Evoluções previstas

O projeto foi concebido para permitir evoluções como:

- Sistema de autenticação de usuários
- Gestão de agendas e responsabilidades
- Registro estruturado de interações
- Integração com IA generativa para mediação de comunicação
- Assistente virtual para apoio a decisões e esclarecimento de dúvidas

---

## 💡 Diferenciais do projeto

- Baseado em **problema real do sistema de justiça**
- Aplicação com potencial de impacto social direto
- Integração potencial com **IA generativa**
- Foco em **mediação de conflitos e usabilidade**
- Desenvolvimento alinhado a práticas de inovação pública

---

## ▶️ Como executar o projeto


Requisitos mínimos:
- Python 3.10+ (ou versão compatível do seu ambiente)

Passos rápidos:

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
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


### 👩‍💻 Autora
Ana Beatriz Kindinger

Desenvolvedora Python / Django
Especialização em Inteligência Artificial Aplicada (UFPR)
Experiência em inovação no setor público (TJPR)

https://www.linkedin.com/in/anakindinger

