# Bulk Certificate Generator

A FastAPI-based backend application for generating certificates in bulk from a predefined certificate template.

The application accepts an event name, event date, and a list of recipients. It validates the recipient data, creates a generation job, generates an individual PDF certificate for each recipient, tracks the generation status, handles individual failures without stopping the remaining certificates, and provides APIs to retrieve generated certificates.

## Features

- Bulk certificate generation
- REST API using FastAPI
- SQLite relational database
- SQLAlchemy ORM
- Pydantic request validation
- Email validation
- PDF certificate generation using ReportLab
- Job status tracking
- Certificate-level status tracking
- Success and failure counters
- Individual failure isolation
- Certificate PDF retrieval
- Swagger/OpenAPI documentation
- Automated API testing using Pytest
- Git/GitHub version control

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend programming language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| SQLite | Relational database |
| SQLAlchemy | ORM and database interaction |
| Pydantic | Request validation |
| ReportLab | PDF certificate generation |
| Pytest | Automated testing |
| HTTPX | API testing |
| Git | Version control |
| GitHub | Source code hosting |

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── certificate_service.py
│   │
│   ├── database.py
│   ├── main.py
│   └── __init__.py
│
├── tests/
│   └── test_api.py
│
├── generated/
├── templates/
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Prerequisites

Make sure the following are installed:

- Python 3.11+
- pip
- Git

Check Python:

```bash
python --version
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/HarunMatthew/bulk-certificate-generator.git
cd bulk-certificate-generator
```

### 2. Create a virtual environment

#### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

The interactive Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/jobs/` | Create a bulk certificate generation job |
| GET | `/api/jobs/{job_id}` | Get job status and progress |
| GET | `/api/jobs/{job_id}/certificates/` | List certificates for a job |
| GET | `/api/certificates/{certificate_id}` | Download a generated certificate |

## API Usage

### 1. Create a Bulk Certificate Job

**Endpoint:**

```http
POST /api/jobs/
```

**Request body:**

```json
{
  "event_name": "Python Backend Workshop",
  "date": "2026-10-08",
  "recipients": [
    {
      "name": "Harun Matthew",
      "email": "harun@example.com"
    },
    {
      "name": "Rahul Kumar",
      "email": "rahul@example.com"
    },
    {
      "name": "Priya Sharma",
      "email": "priya@example.com"
    }
  ]
}
```

**Example Windows CMD request:**

```cmd
curl -X POST "http://127.0.0.1:8000/api/jobs/" -H "Content-Type: application/json" -d "{\"event_name\":\"Python Backend Workshop\",\"date\":\"2026-10-08\",\"recipients\":[{\"name\":\"Harun Matthew\",\"email\":\"harun@example.com\"},{\"name\":\"Rahul Kumar\",\"email\":\"rahul@example.com\"},{\"name\":\"Priya Sharma\",\"email\":\"priya@example.com\"}]}"
```

**Example response:**

```json
{
  "job_id": 1,
  "status": "COMPLETED",
  "total": 3,
  "successful": 3,
  "failed": 0
}
```

### 2. Check Job Status

**Endpoint:**

```http
GET /api/jobs/{job_id}
```

**Example:**

```http
GET /api/jobs/1
```

**Example response:**

```json
{
  "job_id": 1,
  "event_name": "Python Backend Workshop",
  "event_date": "2026-10-08",
  "status": "COMPLETED",
  "total": 3,
  "successful": 3,
  "failed": 0,
  "created_at": "2026-10-08T05:30:00"
}
```

The response provides the total number of recipients, successful certificates, failed certificates, and overall job status.

### 3. Get Certificates for a Job

**Endpoint:**

```http
GET /api/jobs/{job_id}/certificates/
```

**Example:**

```http
GET /api/jobs/1/certificates/
```

**Example response:**

```json
{
  "job_id": 1,
  "certificates": [
    {
      "certificate_id": 1,
      "recipient_name": "Harun Matthew",
      "recipient_email": "harun@example.com",
      "status": "SUCCESS",
      "error": null
    },
    {
      "certificate_id": 2,
      "recipient_name": "Rahul Kumar",
      "recipient_email": "rahul@example.com",
      "status": "SUCCESS",
      "error": null
    },
    {
      "certificate_id": 3,
      "recipient_name": "Priya Sharma",
      "recipient_email": "priya@example.com",
      "status": "SUCCESS",
      "error": null
    }
  ]
}
```

### 4. Retrieve a Generated Certificate

**Endpoint:**

```http
GET /api/certificates/{certificate_id}
```

**Example:**

```http
GET /api/certificates/1
```

If the certificate was generated successfully, the API returns the PDF file with:

```text
Content-Type: application/pdf
```

Generated certificates are stored in:

```text
generated/
```

Example:

```text
generated/
├── 1_Harun_Matthew.pdf
├── 2_Rahul_Kumar.pdf
└── 3_Priya_Sharma.pdf
```

## Validation

Recipient data is validated using Pydantic.

Each recipient must contain:

```json
{
  "name": "Recipient Name",
  "email": "recipient@example.com"
}
```

Validation rules include:

- Event name cannot be empty.
- Recipient name cannot be empty.
- Recipient email must be valid.
- At least one recipient is required.

For invalid input, FastAPI returns:

```text
422 Unprocessable Entity
```

### Invalid email example

```json
{
  "event_name": "Python Workshop",
  "date": "2026-10-08",
  "recipients": [
    {
      "name": "Test User",
      "email": "invalid-email"
    }
  ]
}
```

## Certificate Generation

PDF certificates are generated using ReportLab.

The certificate generation logic is located in:

```text
app/services/certificate_service.py
```

Each certificate contains:

- Certificate title
- Recipient name
- Event name
- Event date

The generated PDF is saved in the `generated/` directory.

## Job Status Tracking

Each generation job tracks:

```text
total
successful
failed
status
created_at
```

Possible job statuses are:

```text
PROCESSING
COMPLETED
COMPLETED_WITH_ERRORS
```

Example:

```text
Total:       5
Successful:  4
Failed:      1
Status:      COMPLETED_WITH_ERRORS
```

## Individual Failure Isolation

Each recipient's certificate is processed independently.

For example:

```text
Recipient 1 → SUCCESS
Recipient 2 → SUCCESS
Recipient 3 → FAILED
Recipient 4 → SUCCESS
Recipient 5 → SUCCESS
```

If one certificate fails, the remaining valid certificates continue to generate.

The failed certificate stores its error message, and the overall job can finish with:

```text
COMPLETED_WITH_ERRORS
```

This prevents one invalid or problematic recipient from stopping the entire bulk generation process.

## Database Design

The application uses SQLite as the relational database and SQLAlchemy as the ORM.

The database contains two main tables.

### Jobs

Stores information about each bulk generation request.

Main fields:

```text
id
event_name
event_date
status
total
successful
failed
created_at
```

### Certificates

Stores information about each generated certificate.

Main fields:

```text
id
job_id
recipient_name
recipient_email
status
file_path
error_message
```

### Relationship

One job can contain multiple certificates:

```text
Job
 ├── Certificate
 ├── Certificate
 └── Certificate
```

The `job_id` field connects each certificate to its corresponding job.

## Design Decisions

### FastAPI

FastAPI was selected because it provides:

- Simple REST API development
- Automatic request validation
- Automatic Swagger/OpenAPI documentation
- Python type-hint support
- Easy API testing

### SQLite

SQLite was selected because the assignment requires a relational database but does not require a production database server.

It provides:

- Simple setup
- No separate database server
- Relational database support
- Easy local development

The database layer can later be migrated to PostgreSQL if required.

### SQLAlchemy

SQLAlchemy is used as the ORM layer to separate database operations from API logic and provide a maintainable database model.

### Pydantic

Pydantic is used to validate incoming API requests before certificate generation begins.

This prevents invalid recipient information from entering the generation process.

### ReportLab

ReportLab is used to generate PDF certificates programmatically.

The PDF generation logic is kept separately inside the certificate service.

### Synchronous Processing

The current implementation uses synchronous processing to keep the solution simple and suitable for the assignment scope.

For a large production system, background processing could be introduced using a task queue such as Celery.

### Individual Error Handling

Each certificate generation is handled independently so that one failure does not stop other valid certificates.

## Testing

Automated API tests are implemented using Pytest and FastAPI's `TestClient`.

Run the tests with:

```bash
pytest
```

The test suite covers:

- Job creation
- Invalid email validation
- Job retrieval
- Certificate listing
- Certificate PDF retrieval

Current test result:

```text
5 passed
```

Example:

```text
tests/test_api.py .....                                             [100%]

5 passed
```

## Complete Workflow

```text
Client
  |
  | POST /api/jobs/
  v
Validate request
  |
  v
Create generation job
  |
  v
Create certificate records
  |
  v
Generate certificates individually
  |
  +------ SUCCESS ------> Save PDF
  |
  +------ FAILURE ------> Save error and continue
  |
  v
Update job status
  |
  v
GET /api/jobs/{job_id}
  |
  v
GET /api/jobs/{job_id}/certificates/
  |
  v
GET /api/certificates/{certificate_id}
  |
  v
Download PDF
```

## GitHub Repository

Repository:

https://github.com/HarunMatthew/bulk-certificate-generator

Clone the project:

```bash
git clone https://github.com/HarunMatthew/bulk-certificate-generator.git
```

## Git Commands

Check project status:

```bash
git status
```

Add changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Update project"
```

Push changes:

```bash
git push
```

## Gitignored Files

The following local files are excluded from Git:

```text
venv/
__pycache__/
*.pyc
certificates.db
generated/
.pytest_cache/
```

This prevents the Python virtual environment, generated certificates, local database, and temporary files from being uploaded to GitHub.

## Future Improvements

Possible future improvements include:

- Background certificate generation
- Redis integration
- Celery/task queue integration
- PostgreSQL database
- Authentication and authorization
- Multiple certificate templates
- Custom certificate designs
- Email delivery
- Cloud file storage
- Pagination for large recipient lists
- Improved progress tracking
- Docker support
- Cloud deployment
- Structured logging
- Additional automated tests

These improvements are outside the current assignment scope.

## Author

**Harun Matthew**

GitHub:

https://github.com/HarunMatthew