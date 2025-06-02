# Simple HTTP API

A lightweight REST API for managing user data with basic CRUD operations. Built with Python and designed for simplicity and ease of use.

## Overview

This API provides endpoints for user management including creation, retrieval, updating, and deletion of user records. All user data is persisted using file-based serialization.

## Project Structure

```
.
├── models/
│   ├── base.py          # Base model with file serialization
│   └── user.py          # User model definition
├── api/v1/
│   ├── app.py           # API entry point and Flask application
│   └── views/
│       ├── index.py     # Status and statistics endpoints
│       └── users.py     # User management endpoints
└── requirements.txt     # Python dependencies
```

### Core Components

#### Models (`models/`)
- **`base.py`**: Foundation class for all API models, handles serialization to file storage
- **`user.py`**: User model with attributes and validation logic

#### API (`api/v1/`)
- **`app.py`**: Flask application entry point with route registration and configuration
- **`views/index.py`**: System endpoints for API health and statistics
- **`views/users.py`**: Complete user CRUD operations and endpoint handlers

## Installation

### Prerequisites
- Python 3.6+
- pip3

### Setup
1. **Clone the repository** (if applicable)
2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

### Starting the Server
```bash
API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```

**Environment Variables:**
- `API_HOST`: Server host address (default: 0.0.0.0)
- `API_PORT`: Server port number (default: 5000)

### Base URL
```
http://localhost:5000/api/v1
```

## API Endpoints

### System Endpoints
| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/api/v1/status` | API health check | Returns API status |
| `GET` | `/api/v1/stats` | API usage statistics | Returns API metrics |

### User Management
| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/users` | List all users | None |
| `GET` | `/api/v1/users/:id` | Get user by ID | `id` (path parameter) |
| `POST` | `/api/v1/users` | Create new user | JSON body (see below) |
| `PUT` | `/api/v1/users/:id` | Update user | `id` (path) + JSON body |
| `DELETE` | `/api/v1/users/:id` | Delete user | `id` (path parameter) |

### Request/Response Format

#### Create User (`POST /api/v1/users`)
**Required Parameters:**
- `email` (string): User's email address
- `password` (string): User's password

**Optional Parameters:**
- `first_name` (string): User's first name
- `last_name` (string): User's last name

**Example Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Update User (`PUT /api/v1/users/:id`)
**Parameters:**
- `first_name` (string): Updated first name
- `last_name` (string): Updated last name

**Example Request:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

## Examples

### Check API Status
```bash
curl http://localhost:5000/api/v1/status
```

### Create a New User
```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "mypassword",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Get All Users
```bash
curl http://localhost:5000/api/v1/users
```

### Update User
```bash
curl -X PUT http://localhost:5000/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "last_name": "Name"
  }'
```

### Delete User
```bash
curl -X DELETE http://localhost:5000/api/v1/users/1
```

## Features

- **RESTful Design**: Follows REST principles for intuitive API usage
- **File-based Storage**: Simple file serialization for data persistence
- **JSON Communication**: All requests and responses use JSON format
- **Error Handling**: Proper HTTP status codes and error messages
- **Modular Structure**: Clean separation of concerns with organized file structure

## Development

The API is built with Flask and follows a modular architecture for easy maintenance and extension. The file-based storage system makes it ideal for development and testing environments.

## Contributing

When contributing to this project:
1. Follow the existing code structure and naming conventions
2. Ensure all endpoints return appropriate HTTP status codes
3. Test all CRUD operations thoroughly
4. Update documentation for any new endpoints or changes
