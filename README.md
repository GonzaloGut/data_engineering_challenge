# Data Engineering Challenge

A lightweight Data Engineering pipeline built with FastAPI and PostgreSQL.

The project ingests CSV files, validates and cleans data, stores valid records in PostgreSQL, separates invalid rows for observability, and exposes analytical REST endpoints.

The solution follows a simplified Medallion Architecture approach:

- Bronze Layer → Raw CSV storage
- Silver Layer → Cleaned and validated PostgreSQL tables
- Gold Layer → Analytical SQL endpoints

## 🔗 Quick Links

- 🚀 **[Live API](https://data-engineering-api-235042863861.us-central1.run.app/docs)**
- 📖 **[Medium Article](https://medium.com/@gonzaloglr23/building-an-end-to-end-data-engineering-api-with-fastapi-postgresql-docker-and-google-cloud-84137b3fb8ad)**

## Architecture

- FastAPI REST API
- PostgreSQL relational database
- Docker containerization
- Batch CSV ingestion
- Data validation and cleaning pipeline
- Analytical SQL endpoints
- Automated tests with pytest

## Tech Stack

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pandas
- Docker
- Pytest

## Project Structure

```text
data_engineering_challenge/
│
├── app/
│   ├── api/
│   ├── database/
│   ├── models/
│   ├── utils/
│   └── main.py
│
├── storage/
│   ├── bronze/
│   └── errors/
│
├── tests/
│
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

## Running the Project

### 1. Clone repository

```bash
git clone <your_repo_url>
cd data_engineering_challenge
```


### 2. Configure Environment Variables
Create a `.env` file in the project root:

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=password0526
POSTGRES_DB=challenge_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

### 3. Start Docker Containers

```bash
docker compose up --build
```

### 4. Access Swagger Documentation

```
http://localhost:8000/docs
```

## API Endpoints

### Upload Endpoints

- POST `/upload/departments`
- POST `/upload/jobs`
- POST `/upload/employees`

### Analytics Endpoints

- GET `/analytics/employees_by_quarter`:
Returns the number of employees hired for each job and department in 2021 divided by quarter.

- GET `/analytics/departments_above_mean`:
Returns departments that hired more employees than the average number of hires in 2021.

## Data Validation & Cleaning

The ingestion pipeline performs:

- CSV format validation
- Datetime validation
- Numeric type cleaning
- Invalid rows separation
- Foreign key validation
- Partial ingestion of valid records

Invalid rows are automatically stored for observability and troubleshooting.

## Testing

Run automated tests:

```bash
pytest
``` 

Current tests include:

- API availability
- Analytics endpoints
- Invalid file upload validation

## Medallion Architecture

### Bronze Layer
Stores raw uploaded CSV files.

```
storage/bronze/
```

### Silver Layer
Stores cleaned and validated records in PostgreSQL.

### Gold Layer
Provides analytical REST endpoints using SQL aggregations.

## Future Improvements

- CI/CD pipelines
- Cloud deployment automation
- Data quality monitoring
- Authentication & authorization
- Orchestration workflows
- Data warehouse integration

## Author

Gonzalo Gutierrez
