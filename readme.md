# Overview

Sandbox FastAPI server, which runs in a VS Code dev container. Created for educational purposes only.

This is just meant to illustrate a potential method of file organization or project structure for a small team looking to avoid merge conflicts.

What it's missing is a provider base class or protocol that abstracts the same method call to point at different services.

For example:
- ProviderTelecom -> ProviderSprint -> callHome
- ProviderTelecom -> ProviderAtt -> callHome

# Setup

From the `root` of the project `directory`: 
- Populate the `env.sample` file with your desired `bcrypt` hashing algorithm and secret.
- `cp env.sample .env`

# Alembic
Upgrade DB tables:
```
   alembic revision --autogenerate -m "Initial migration"
```
