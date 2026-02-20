# Diabetes Risk Prediction System

This is a complete end-to-end MLOps system for predicting diabetes risk based on patient data. The system includes data pipeline, feature engineering, model training, deployment, monitoring, and CI/CD.

## Features

- Data pipeline with DVC for versioning
- Feature engineering with Feast feature store
- Model training with Scikit-learn and MLflow
- Pipeline orchestration with Apache Airflow
- REST API with FastAPI
- Monitoring with Prometheus and Grafana
- Containerized services with Docker
- CI/CD with GitHub Actions
- Storage with PostgreSQL and MinIO

## Architecture

```
┌─────────────┐    ┌────────────────┐    ┌──────────────┐
│   Data      │───▶│ Feature Store  │───▶│   Model      │
│   Pipeline  │    │  (Feast)       │    │ Training     │
└─────────────┘    └────────────────┘    └──────────────┘
                                                │
                        ┌───────────────────────┘
                        ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Airflow    │───▶│ Model        │───▶│  FastAPI     │
│ Orchestration│    │ Registry     │    │  Serving     │
└─────────────┘    │ (MLflow)     │    └──────────────┘
                   └──────────────┘           │
                        │                     │
                        ▼                     ▼
              ┌──────────────┐    ┌─────────────────────┐
              │  Monitoring  │    │  CI/CD Pipeline     │
              │ (Prometheus  │    │ (GitHub Actions)    │
              │ & Grafana)   │    └─────────────────────┘
              └──────────────┘
```

## Project Structure

```
├── data/                          # Dataset and DVC files
├── models/                        # Trained models
├── notebooks/                     # Jupyter notebooks for exploration
├── src/                           # Source code
│   ├── api/                       # FastAPI application
│   ├── airflow/                   # Airflow DAGs and configuration
│   ├── data_pipeline/             # Data processing scripts
│   ├── feature_store/             # Feast feature definitions
│   ├── model_training/            # Model training scripts
│   ├── model_registry/            # MLflow model registry utilities
│   ├── monitoring/                # Prometheus and Grafana configs
│   ├── docker/                    # Docker configurations
│   └── storage/                   # Storage initialization scripts
├── tests/                         # Unit and integration tests
├── docs/                          # Documentation files
├── .github/workflows/             # GitHub Actions workflows
├── docker-compose.yml             # Docker Compose configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Quick Start (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd diabetes-risk-prediction-system
```

2. Run with Docker (Single command setup):
```bash
docker-compose up -d
```

3. Access services:
- API: http://localhost:8000
- MLflow: http://localhost:5000
- Airflow: http://localhost:8080 (login: admin/admin)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (login: admin/admin)

4. Try a prediction:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 2,
    "glucose": 120,
    "blood_pressure": 70,
    "skin_thickness": 25,
    "insulin": 100,
    "bmi": 28.5,
    "diabetes_pedigree": 0.5,
    "age": 35
  }'
```

## Detailed Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Git

### Option 1: Full Docker Deployment (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd diabetes-risk-prediction-system
```

2. Start all services:
```bash
docker-compose up -d
```

3. Wait 2-3 minutes for services to initialize

4. Verify services are running:
```bash
docker-compose ps
```

### Option 2: Manual Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

2. Initialize DVC:
```bash
dvc init
dvc add data/diabetes_data.csv
```

3. Start required services manually:

**Start PostgreSQL:**
```bash
docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:13
```

**Start MinIO:**
```bash
docker run -d --name minio -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio server /data --console-address ":9001"
```

4. Initialize storage:
```bash
python src/storage/init_storage.py
```

5. Start MLflow tracking server:
```bash
mlflow server --host 0.0.0.0 --port 5000 \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns
```

6. Start Airflow:
```bash
# Set Airflow home directory
export AIRFLOW_HOME=$(pwd)/src/airflow

# Initialize Airflow database
airflow db init

# Create admin user
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com

# Start Airflow scheduler and webserver in separate terminals
airflow scheduler
airflow webserver
```

7. Start API:
```bash
python src/api/main.py
```

## Usage Guide

### API Endpoints

- `GET /` - Root endpoint showing API status
- `GET /health` - Health check with model loading status
- `POST /predict` - Predict diabetes risk for patient data
- `GET /model/info` - Get information about loaded model
- `GET /metrics` - Prometheus metrics endpoint

### Making Predictions

Example request:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 2,
    "glucose": 120,
    "blood_pressure": 70,
    "skin_thickness": 25,
    "insulin": 100,
    "bmi": 28.5,
    "diabetes_pedigree": 0.5,
    "age": 35
  }'
```

Response:
```json
{
  "prediction": 1,
  "probability": 0.78,
  "confidence": 0.85
}
```

### Training Models

To train a new model:
```bash
python src/model_training/train_model.py
```

### Running Airflow Pipeline

1. Access Airflow UI at http://localhost:8080
2. Log in with credentials (admin/admin)
3. Find the "diabetes_prediction_pipeline" DAG
4. Toggle the switch to "On"
5. Click the "Play" button to trigger a manual run
6. Monitor progress in the Graph View or Tree View

### Monitoring with Grafana

1. Access Grafana at http://localhost:3000
2. Log in with credentials (admin/admin)
3. Navigate to Dashboards → Manage
4. Open the "Diabetes Prediction API" dashboard
5. View real-time metrics:
   - API health status
   - Prediction volume
   - Model confidence levels
   - Request latencies

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=html
```

### Code Quality

```bash
# Linting
flake8 .

# Format code
black .
```

### CI/CD Process

The project uses GitHub Actions for continuous integration:
1. Tests run automatically on every push
2. Code quality checks are performed
3. Docker images are built for releases
4. Deployment can be triggered manually

To trigger a release:
1. Create a commit with "[release]" in the message
2. Push to the main branch
3. GitHub Actions will automatically deploy

## Advanced Configuration

### Environment Variables

Create a `.env` file in the project root:
```env
MLFLOW_TRACKING_URI=http://localhost:5000
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

### Scaling Considerations

For production deployments:
1. Replace SQLite with PostgreSQL for MLflow backend
2. Use Kubernetes instead of Docker Compose
3. Add load balancers for high availability
4. Implement backup and disaster recovery
5. Add authentication and authorization

## Documentation

Additional documentation is available in the `docs/` directory:
- `docs/index.md` - Comprehensive system documentation
- `docs/quickstart.md` - Quick start guide
- `SUMMARY.md` - Technical summary

## Contributing

We welcome contributions to improve the Diabetes Risk Prediction System:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows our standards:
- Use Python Black for formatting
- Write docstrings for all functions
- Include unit tests for new functionality
- Keep dependencies minimal

## Support

For support, please:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information
4. Include error messages and steps to reproduce

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python, FastAPI, MLflow, Apache Airflow, and other open-source technologies
- Healthcare dataset based on the National Institute of Diabetes and Digestive and Kidney Diseases
- Inspired by MLOps best practices and real-world deployment patterns
