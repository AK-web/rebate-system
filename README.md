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
   - Django:
      ```bash
      pip install django
      ```
   - djangorestframework:
     ```bash
      pip install djangorestframework
     ```

2. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Run the application locally:
   ```bash
   python .\manage.py runserver
   ```

---

# API Documentation

## 1. Create Rebate Program

### Endpoint
*POST* `http://127.0.0.1:8000/api/create-rebate-program/`

### Request Body
```json
{
    "program_name": "Diwali Discounts",
    "rebate_percentage": 30,
    "start_date": "2024-12-01",
    "end_date": "2024-12-31",
    "eligibility_criteria": "Valid for transactions over $50"
}
```

### Response
#### Success Response
```json
{
    "id": 5,
    "program_name": "Diwali Discounts",
    "rebate_percentage": "30.00",
    "start_date": "2024-12-01",
    "end_date": "2024-12-31",
    "eligibility_criteria": "Valid for transactions over $50",
    "is_active": true
}
```

---

## 2. Submit Transaction

### Endpoint
*POST* `http://127.0.0.1:8000/api/submit-transaction/`

### Request Body
```json
{
    "transaction_id": "T12345",
    "amount": 100,
    "transaction_date": "2024-12-05T10:30:00Z",
    "rebate_program": 1
}
```

### Response
#### Success Response
```json
{
    "id": 6,
    "rebate_amount": 10.0,
    "transaction_id": "T12345",
    "amount": "100.00",
    "transaction_date": "2024-12-05T10:30:00Z",
    "rebate_program": 1
}
```

---

## 3. Claim Rebate

### Endpoint
*POST* `http://127.0.0.1:8000/api/claim-rebate/`

### Request Body
```json
{
  "claim_id": "CLAIM12345", 
  "transaction": "4",  
  "claim_amount": 50.0,
  "claim_status": "pending"
}
```

### Responses
#### Error Response
```json
{
    "transaction": [
        "rebate claim with this transaction already exists."
    ]
}
```

#### Success Response
```json
{
    "id": 5,
    "claim_id": "CLAIM12345",
    "claim_amount": "50.00",
    "claim_status": "pending",
    "claim_date": "2024-12-14T07:26:37.855334Z",
    "notes": null,
    "transaction": 6
}
```

---

## 4. Generate Rebate Report

### Endpoint
*POST* `http://127.0.0.1:8000/api/rebate-report/`

### Request Body
```json
{
    "start_date": "2023-01-01",
    "end_date": "2025-12-31"
}
```

### Response
#### Success Response
```json
{
    "total_claims": 4,
    "total_approved_amount": 0
}
```

---

## 5. Calculate Rebate for a Transaction

### Endpoint
*GET* `http://127.0.0.1:8000/api/calculate-rebate/TXN123/`

### Expected Response
#### Success Response
```json
{
    "transaction_id": "T12345",
    "rebate_amount": 10.0
}
```

---

## Suggestions on how to make the system scalable and efficient in a production environment:

### 1. Optimize Database and Queries
### 
Add indexes on `created_at` and other frequently filtered fields. Use efficient date filtering `(created_at__gte, created_at__lte)` instead of converting to date.
### 2. Implement Caching
#### 
Cache API responses for commonly queried date ranges using Django’s caching framework.Use HTTP caching headers (ETag, Last-Modified) to reduce redundant client requests.
### 3. Scale Infrastructure
#### 
Deploy behind a load balancer and use auto-scaling to handle high traffic. Use containerized solutions (e.g., Docker, Kubernetes) for horizontal scaling.
### 4. Enhance API Efficiency
#### 
Restrict the date range for queries to prevent large dataset processing. Offload heavy computations to asynchronous workers (e.g., Celery with Redis).

