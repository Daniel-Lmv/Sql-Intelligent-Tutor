# ITS SQL - Sistema Tutor Inteligente para Ensino de SQL

## Descrição

Este projeto consiste no desenvolvimento de um Sistema Tutor Inteligente (ITS) voltado para o ensino de SQL. O sistema busca acompanhar o desempenho do estudante, identificar dificuldades em conceitos específicos e recomendar atividades adequadas ao seu nível de conhecimento.

O domínio abordado pelo tutor contempla os principais conceitos de SQL:

* SELECT
* WHERE
* ORDER BY
* Funções de Agregação
* GROUP BY
* HAVING
* JOINS
* SUBQUERIES

O sistema utiliza um modelo de proficiência para acompanhar a evolução do aluno e um conjunto de exercícios práticos para avaliar seu conhecimento.

---

## Estrutura do Projeto

```text
ITS-SQL/

├── backend/
│
│   ├── database/
│   │
│   │   ├── connection.py
│   │   ├── init_db.py
│   │   ├── create_exercises_db.py
│   │
│   │   ├── usuarios_repository.py
│   │   ├── conceitos_repository.py
│   │   ├── questoes_repository.py
│   │   ├── proficiencia_repository.py
│   │   └── respostas_repository.py
│   │
│   │   ├── its.db
│   │   └── exercises.db
│   │
│   ├── domain/
│   │
│   ├── services/
│   │
│   ├── tests/
│   │
│   ├── requirements.txt
│   │
│   └── main.py
│
├── frontend/
│
├── .gitignore
│
└── README.md
```

---

## Tecnologias Utilizadas

### Backend

* Python 3.x
* SQLite
* FastAPI (planejado)

### Banco de Dados

* SQLite

### Controle de Versão

* Git
* GitHub

---

## Configuração do Ambiente

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>

cd ITS-SQL/backend
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv
```

### 3. Ativar Ambiente Virtual

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## Criação dos Bancos de Dados

O projeto utiliza dois bancos SQLite:

### its.db

Responsável por armazenar:

* Usuários
* Questões
* Conceitos
* Proficiência dos alunos
* Histórico de respostas

### exercises.db

Responsável por armazenar os dados utilizados nas consultas SQL dos exercícios.

---

### Criar o Banco do ITS

```bash
python database/init_db.py
```

---

### Criar o Banco de Exercícios

```bash
python database/create_exercises_db.py
```

---

## Modelo de Dados do ITS

### usuarios

Armazena informações dos estudantes.

### conceitos

Armazena os conceitos do domínio SQL.

### questoes

Armazena os exercícios disponíveis.

### proficiencia

Armazena o nível de domínio de cada aluno em cada conceito.

### respostas

Armazena o histórico de respostas dos alunos.

---

## Banco de Exercícios

O banco de exercícios contém tabelas utilizadas para as consultas SQL:

### clientes

Informações de clientes.

### produtos

Informações de produtos.

### pedidos

Histórico de pedidos realizados.

### departamentos

Departamentos da empresa fictícia.

### funcionarios

Funcionários associados aos departamentos.

Essas tabelas permitem criar exercícios envolvendo:

* Seleção de dados
* Filtros
* Ordenação
* Agrupamentos
* Funções de agregação
* Junções
* Subconsultas

---

## Execução de Testes

Os testes podem ser executados individualmente pela pasta tests.

Exemplo:

```bash
python tests/test_database.py
```

---

## Objetivo Pedagógico

O sistema busca:

1. Avaliar o conhecimento inicial do aluno por meio de um teste diagnóstico.
2. Manter um modelo de proficiência para cada conceito de SQL.
3. Atualizar o progresso do aluno conforme suas respostas.
4. Recomendar exercícios adequados ao nível de conhecimento identificado.
5. Auxiliar o estudante no aprendizado gradual dos conceitos de SQL.

---

## Autores

Projeto desenvolvido para a disciplina de Sistemas Tutores Inteligentes.

Integrantes do grupo:

* Daniel Limaverde
* Matheus Rodrigues
* José Victor
* Marcelo José

```
```
