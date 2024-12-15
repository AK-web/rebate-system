# rebate-system : Setup Instructions

## Docker Setup

1. Generate the `requirements.txt` file with installed Python dependencies:
   ```bash
   pip freeze > requirements.txt
   ```

2. Build the Docker image:
   ```bash
   docker build -t rebate-app .
   ```

3. Run the Docker container:
   ```bash
   docker run -p 8000:8000 rebate-app
   ```

## Local Setup

1. Install the following prerequisites:
   - Python (version 3.13.1)
   - Django
   - djangorestframework

2. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Run the application locally:
   ```bash
   python .\manage.py runserver
   ```
   
