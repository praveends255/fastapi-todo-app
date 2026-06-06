# FastAPI Todo Management API

A secure and scalable Todo Management REST API built using FastAPI, MySQL, SQLModel, JWT Authentication, and Docker.

This project demonstrates modern backend development practices including authentication, authorization, database integration, API validation, and containerization. Users can register, log in, manage their personal tasks, and securely access only their own data through protected API endpoints.

## Key Features

### Authentication & Security

* User Registration and Login
* JWT-based Authentication
* Password Hashing using secure algorithms
* Protected Endpoints
* User-level Authorization

### Todo Management

* Create New Tasks
* Retrieve All Personal Tasks
* Retrieve Task by ID
* Filter Tasks by Priority
* Update Existing Tasks
* Delete Tasks
* Mark Tasks as Completed

### User Management

* Change Password
* Secure User Identity Handling
* Personal Task Isolation

### Database Integration

* MySQL Database
* SQLModel ORM
* Automatic Table Creation
* Transaction Management

### Backend Architecture

* Modular Router-Based Structure
* Request and Response Schemas
* Dependency Injection
* Environment Variable Configuration
* Error Handling

### DevOps

* Dockerized Application
* Docker Compose Support
* Environment-Based Configuration

## Tech Stack

| Technology | Purpose             |
| ---------- | ------------------- |
| FastAPI    | REST API Framework  |
| SQLModel   | Database ORM        |
| MySQL      | Relational Database |
| JWT        | Authentication      |
| Docker     | Containerization    |
| Python     | Backend Development |

## API Endpoints

### Authentication

* POST `/auth/signup`
* POST `/auth/login`

### User

* PUT `/user/change_password`

### Todo

* POST `/todo/create`
* GET `/todo/all`
* GET `/todo/{todo_id}`
* GET `/todo/by_priority/{priority}`
* PUT `/todo/update/{todo_id}`
* DELETE `/todo/delete/{todo_id}`

## Running the Project

### Using Docker

```bash
docker-compose up --build
```

### Access API Documentation

```text
http://localhost:8000/docs
```

## Skills Demonstrated

* REST API Development
* FastAPI Framework
* JWT Authentication & Authorization
* Secure Password Management
* MySQL Database Design
* SQLModel ORM
* CRUD Operations
* API Validation
* Dependency Injection
* Docker Containerization
* Backend Project Structuring
* Environment Variable Management

## Future Improvements

* Refresh Token Support
* Role-Based Access Control (RBAC)
* Pagination and Search
* Unit & Integration Testing
* CI/CD Pipeline Integration
* Cloud Deployment
