# Overview

Sandbox FastAPI server, which runs in a VS Code dev container. Created for educational purposes only.

# Setup

From the `root` of the project `directory`: 
- Populate the `env.sample` file with your desired `bcrypt` hashing algorithm and secret.
- `cp env.sample .env`

# Alembic
Upgrade DB tables:
```
   alembic revision --autogenerate -m "Initial migration"
```