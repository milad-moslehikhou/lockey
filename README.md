# Lockey

**Lockey** is a secret management application designed to securely handle sensitive information such as passwords, API keys, and confidential data. It provides a streamlined interface and robust backend to ensure your secrets are managed and stored securely.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## Features

- **Secure Secret Storage**: Lockey securely stores your sensitive data.
- **User Authentication**: Secure login system for user-specific secret management.
- **Role-Based Access Control**: Manage who can view or modify certain secrets.
- **Dashboard**: User-friendly interface to view, create, and manage secrets.
- **API Support**: Access secrets programmatically through a REST API.

## Tech Stack

- **Frontend**: React
- **Backend**: Python (Django)
- **Database**: MySql / SQLite
- **Containerization**: Docker
- **Reverse Proxy**: NGINX
- **Version Control**: Git

## Installation

### Prerequisites

- Ensure Docker is installed on your system.

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/milad-moslehikhou/lockey.git
   cd lockey
   ```

   **Frontend**:
   follow instructions in `https://github.com/milad-moslehikhou/lockey-front/README.md`

2. Build and run the app using Docker:

   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: `http://localhost:8080`
   - Backend API: `http://localhost:8080/api/v1/`

## Usage

1. Visit `http://localhost:8080` and log in using your credentials.
2. Create, view, or manage your secrets from the dashboard.
3. Use the REST API to programmatically interact with secrets (see [API Endpoints](#api-endpoints)).

## API Endpoints

For more information you can see api documents page in `/api/v1/swagger`
