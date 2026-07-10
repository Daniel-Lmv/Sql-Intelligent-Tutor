# System Architecture

## Overview

The SQL AI Tutor follows a client-server architecture composed of a web frontend, a FastAPI backend, an SQLite database and an AI tutoring module.

## Components

### Frontend

Responsible for:

- Student authentication
- Dashboard
- Diagnostic assessment
- SQL laboratory
- Tutor interface

### Backend

Implemented using FastAPI.

Main responsibilities:

- User authentication
- Diagnostic evaluation
- Lesson management
- SQL validation
- AI tutor integration

### Database

SQLite database storing:

- Users
- Questions
- Lessons
- Student progress
- Laboratory exercises

### AI Tutor

Uses a Large Language Model to:

- Answer questions
- Explain SQL concepts
- Provide personalized feedback
- Guide students through exercises

## Architecture Diagram

<p align="center">
  <img src="assets/architecture.svg" width="100%">
</p>