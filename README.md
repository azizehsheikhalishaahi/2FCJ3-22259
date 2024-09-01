# Ads Manager

this is a system where users can post Ads and also comment on other people's Ads.

## Table of Contents

 - [Features](#features)
 - [Requirements](#requirements)
 - [Installation](#installation)
 - [Configuration](#configuration)
 - [Usage](#usage)
 - [API Documentation](#api-documentation)
 - [Testing](#testing)

## Features

### Business Spec

- Users should be authenticated to do actions like adding Ads and comments.
- Users can register with a unique email as username and password.
- Each user can only comment on an Ad just once.
- Users can see Ads and its related comments without being logged in to the system.
- Users can delete and edit their own Ads.
 
### Technical Spec

- This should be a restful API using one of the popular python web frameworks like Django, Flask, or FastAPI and There is no need for implementing UI.
- Use PostgreSQL as database.
- Use ORM.
- Write Tests for your APIs.
- Make sure you are using an OpenAPI Specification.
- Write a proper README file to set up and run the project.
- Push the code on a public repository on Git source control and commit regularly the code changes.

## Requirements

- Python 3.x
- Django 5.x
- PostgreSQL >12

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/azizehsheikhalishaahi/2FCJ3-22259.git
   cd 2FCJ3-22259
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   Create a PostgreSQL database and update the `DATABASES` setting in `settings.py` or in your `.env` file.

   ```bash
   psql
   CREATE DATABASE yourdbname;
   ```

5. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

## Configuration

To configure environment-specific settings, create a `.env` file in the project root. Here’s an example `.env` file:

```bash
DATABASE_NAME=dbname
DATABASE_USER=dbuser
DATABASE_PASSWORD=dbpass
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## Usage

- **Admin Panel:** Go to `http://127.0.0.1:8000/admin/` to access the Django admin panel.

## API Documentation

This project uses OpenAPI for API documentation. You can view the documentation by navigating to http://127.0.0.1:8000/swagger/ .

## Testing

To run tests, use the following command:

```bash
python manage.py test
```

## Contact