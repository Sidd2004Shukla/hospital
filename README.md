# Hospital Appointment Management API

A robust, containerized REST API built with FastAPI for managing hospital appointments, doctors, and patients. This system includes strict business rules to prevent overlapping appointments and is fully backed by a CI/CD pipeline using GitHub Actions.

## 🚀 Features

- **Patient Management:** Create and retrieve patient records.
- **Doctor Management:** Create and retrieve doctor profiles.
- **Appointment Scheduling:** Book appointments with built-in validation to prevent overlapping time slots for the same doctor.
- **Database Migrations:** Automated schema management using Alembic.
- **Containerized:** Ready-to-deploy Docker configuration.
- **CI/CD:** Automated testing (Pytest), linting (Ruff), security scanning (Bandit), and Docker Hub publishing via GitHub Actions.

## 🛠️ Technology Stack

- **Framework:** FastAPI, Pydantic
- **Database:** SQLite (Default), SQLAlchemy (ORM)
- **Migrations:** Alembic
- **Package Manager:** Poetry
- **Testing:** Pytest, pytest-cov
- **Linting & Security:** Ruff, Bandit
- **Containerization:** Docker

