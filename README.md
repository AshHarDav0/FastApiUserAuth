# FastApiUserAuth

FastApiUserAuth is a Python-based project that provides user authentication functionality using FastAPI and SQLAlchemy. It uses Docker for containerization and Pytest for running tests.

## Installation

Clone the project:

```bash
git clone https://github.com/AshHarDav0/FastApiUserAuth.git
cd FastApiUserAuth
```

## Build and start the project
```commandline
docker-compose -f docker-compose.yml up --build
```

## Swagger UI
```commandline
http://localhost:8000/docs
```

# For Developers

## Use pre-commit in local development
### Create testing virtual environment in project directory
``` python3 -m venv testenv```

### Activate test environment
#### On Linux
``` source testenv/bin/activate```
#### On Windows
``` testenv\Scripts\activate```

### Install pre-commit
``` pip install pre-commit```

### Install pre-commit hooks
``` pre-commit install```

### Export needed environment variables for pre-commit to work
``` export CONTAINER_NAME=fastapiuserauth_app_1```

### Now after each commit, pre-commit will run and check for any issues in the code.