# Diabetes Risk Prediction System Documentation

This documentation provides comprehensive information about the Diabetes Risk Prediction System, including architecture, setup instructions, and usage guidelines.

## Table of Contents

1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Components Overview](#components-overview)
4. [Setup and Installation](#setup-and-installation)
5. [Usage Guide](#usage-guide)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)

## Introduction

The Diabetes Risk Prediction System is a complete MLOps solution designed to predict diabetes risk based on patient medical data. The system follows industry best practices for machine learning operations, ensuring reproducibility, scalability, and reliability.

Key features include:
- Automated data pipeline with versioning
- Feature engineering and storage
- Model training with experiment tracking
- Model registry for version management
- Automated pipeline orchestration
- RESTful API for predictions
- Comprehensive monitoring and alerting
- Containerized deployment

## System Architecture

The system follows a microservices architecture with the following components:

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

## Components Overview

### 1. Data Pipeline (`src/data_pipeline/`)

Responsible for ingesting, validating, and preprocessing patient data.

Key features:
- Data validation with constraint checking
- Missing value imputation
- Feature scaling and normalization
- Train/test data splitting
- DVC integration for version control

### 2. Feature Engineering (`src/feature_store/`)

Implements feature engineering using Feast feature store.

Key features:
- Feature definitions and views
- Offline and online feature computation
- Feature versioning
- Integration with data pipeline

### 3. Model Training (`src/model_training/`)

Handles model training and experiment tracking with MLflow.

Key features:
- Scikit-learn model implementations
- Hyperparameter tuning with GridSearchCV
- Cross-validation and evaluation
- MLflow integration for experiment tracking

### 4. Model Registry (`src/model_registry/`)

Manages model versions and deployment stages using MLflow Model Registry.

Key features:
- Model versioning
- Stage transitions (Staging, Production)
- Model metadata management
- Deployment tracking

### 5. Pipeline Orchestration (`src/airflow/`)

Automates the entire MLOps pipeline using Apache Airflow.

Key features:
- DAG definitions for workflow automation
- Task dependency management
- Error handling and retries
- Schedule-based execution

### 6. Model Serving (`src/api/`)

Exposes machine learning models through a REST API using FastAPI.

Key features:
- Real-time prediction endpoints
- Input validation and error handling
- Metrics collection and monitoring
- Health checks and status reporting

### 7. Monitoring (`src/monitoring/`)

Provides visibility into system performance using Prometheus and Grafana.

Key features:
- API performance metrics
- Prediction volume tracking
- Model confidence monitoring
- Custom dashboards

### 8. Storage (`src/storage/`)

Manages persistent storage using PostgreSQL and MinIO.

Key features:
- Metadata storage with PostgreSQL
- Artifact storage with MinIO
- Database initialization scripts
- Backup and recovery procedures

## Setup and Installation

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Git
- At least 4GB RAM recommended

### Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd diabetes-risk-prediction-system
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access services:
- API: http://localhost:8000
- MLflow: http://localhost:5000
- Airflow: http://localhost:8080
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

### Manual Installation

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

3. Start services individually as described in the README.

## Usage Guide

### Making Predictions

Send a POST request to the `/predict` endpoint with patient data:

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
  "probability": 0.85,
  "confidence": 0.9
}
```

### Training Models

To train a new model:
```bash
python src/model_training/train_model.py
```

This will:
1. Load and preprocess data
2. Train a model using scikit-learn
3. Evaluate model performance
4. Log results to MLflow

### Managing Model Versions

Register a model in the registry:
```bash
python src/model_registry/register_model.py
```

Transition a model to production:
```python
from src.model_registry.register_model import transition_to_production
transition_to_production("diabetes-predictor", 1)
```

### Running Pipelines

1. Access Airflow UI at http://localhost:8080
2. Enable the `diabetes_prediction_pipeline` DAG
3. Trigger the DAG manually or wait for scheduled execution

The pipeline includes:
- Data ingestion and validation
- Feature engineering
- Model training and evaluation
- Model registration

## Monitoring and Maintenance

### Grafana Dashboards

Access Grafana at http://localhost:3000 with credentials (admin/admin):

Dashboard features:
- API health status
- Prediction volume and rates
- Model confidence tracking
- Error rate monitoring
- Latency metrics

### Alerts

Configure alerts in Prometheus:
- High error rates
- Low model confidence
- API downtime
- Resource utilization thresholds

### Maintenance Tasks

Regular maintenance includes:
- Database backups
- Log rotation
- Model retraining
- Performance optimization
- Security updates

## Troubleshooting

### Common Issues

1. **Services not starting**
   - Check Docker logs: `docker-compose logs <service>`
   - Verify ports are not in use
   - Ensure sufficient system resources

2. **Model loading errors**
   - Verify MLflow tracking server is accessible
   - Check model registry for registered models
   - Confirm model artifacts are available

3. **Connection timeouts**
   - Check network connectivity between services
   - Increase timeout values in configuration
   - Verify service dependencies are running

### Debugging Steps

1. Check service logs:
```bash
docker-compose logs api
docker-compose logs mlflow-server
```

2. Verify service health:
```bash
curl http://localhost:8000/health
curl http://localhost:5000/health
```

3. Check MLflow experiments:
- Access MLflow UI at http://localhost:5000
- Verify experiment runs are logged correctly

## Contributing

We welcome contributions to improve the Diabetes Risk Prediction System. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes with clear messages
4. Add tests for new functionality
5. Submit a pull request

Follow our coding standards:
- Use Python Black for code formatting
- Write docstrings for all functions
- Include unit tests for new features
- Document configuration changes
