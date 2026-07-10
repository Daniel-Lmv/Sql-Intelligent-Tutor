# Database Design

## Overview

The SQL AI Tutor uses **SQLite** as its relational database management system. The database stores user information, diagnostic assessments, learning progress, laboratory exercises, and supporting datasets used throughout the tutoring process.

---

# Entity Relationship Overview

The database is organized around six main components:

- Users
- Learning Concepts
- Diagnostic Questions
- Laboratory Questions
- Student Progress
- Student Answers

Additionally, the project includes a historical FIFA World Cup dataset used during SQL laboratory exercises.

---

# Database Schema

## usuarios

Stores registered students.

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Unique user identifier |
| nome | TEXT | Student name |
| email | TEXT | Student email address |

---

## conceitos

Defines the SQL concepts covered by the tutoring system.

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Concept identifier |
| nome | TEXT | Concept name |
| descricao | TEXT | Description of the concept |

Current concepts include:

- SELECT
- WHERE
- ORDER BY
- Aggregations
- GROUP BY
- HAVING
- JOINS
- SUBQUERIES

---

## questoes

Stores the theoretical multiple-choice questions used during the learning process.

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Question identifier |
| conceito_id | INTEGER | Associated SQL concept |
| enunciado | TEXT | Question statement |
| alternativa_a | TEXT | Option A |
| alternativa_b | TEXT | Option B |
| alternativa_c | TEXT | Option C |
| alternativa_d | TEXT | Option D |
| resposta_correta | TEXT | Correct answer |
| dificuldade | INTEGER | Difficulty level |

---

## questoes_diagnostico

Contains the fixed diagnostic assessment presented to students before the tutoring process begins.

Unlike the regular question bank, diagnostic questions are presented in a predefined order and are used to estimate the student's initial knowledge level.

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Question identifier |
| ordem | INTEGER | Presentation order |
| conceito_id | INTEGER | SQL concept |
| enunciado | TEXT | Question statement |
| resposta_correta | TEXT | Correct answer |
| dificuldade | INTEGER | Difficulty level |

---

## laboratorio_questoes

Stores practical SQL laboratory exercises.

Instead of multiple-choice answers, each exercise contains a reference SQL query used to validate the student's solution.

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Exercise identifier |
| conceito_id | INTEGER | SQL concept |
| enunciado | TEXT | Exercise description |
| gabarito_sql | TEXT | Reference SQL solution |

---

## proficiencia

Tracks each student's mastery level for every SQL concept.

Each user has one proficiency value for each concept.

| Field | Type | Description |
|-------|------|-------------|
| usuario_id | INTEGER | Student identifier |
| conceito_id | INTEGER | SQL concept |
| nivel | REAL | Estimated proficiency score |

Composite Primary Key:

```
(usuario_id, conceito_id)
```

---

## respostas

Stores every answer submitted by students.

This table allows the system to monitor learning progress and estimate proficiency.

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Answer identifier |
| usuario_id | INTEGER | Student |
| questao_id | INTEGER | Question |
| resposta_aluno | TEXT | Submitted answer |
| acertou | INTEGER | Correct (1) or Incorrect (0) |
| data_resposta | DATETIME | Submission timestamp |

---

## historico_copas

Contains historical FIFA World Cup data used during SQL laboratory activities.

Students execute SQL queries over this dataset to solve practical exercises involving filtering, aggregation, grouping and joins.

Example attributes include:

- Year
- Host country
- Champion
- Runner-up
- Goals scored
- Attendance
- Golden Ball
- Golden Glove
- Top scorer

---

# Entity Relationships

<p align="center">
  <img src="assets/database_architecture.svg" width="100%">
</p>

---

# Design Decisions

The database was intentionally designed to separate:

- Diagnostic assessment
- Learning activities
- Student progress
- Practical laboratory exercises

This separation simplifies maintenance, improves scalability and allows new SQL concepts and exercises to be added without modifying the existing schema.

---

# Future Improvements

Potential database improvements include:

- Migration from SQLite to PostgreSQL
- User roles (student/instructor)
- Exercise versioning
- Learning analytics tables
- Session history
- Performance metrics
- Automatic feedback storage