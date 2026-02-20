# Quick Start Guide

Get up and running with the Diabetes Risk Prediction System in minutes.

## Prerequisites

- Docker and Docker Compose installed
- Git
- At least 4GB RAM available

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd diabetes-risk-prediction-system
```

## Step 2: Start Services with Docker

```bash
docker-compose up -d
```

This command starts all services:
- API server on port 8000
- MLflow tracking server on port 5000
- Airflow on port 8080
- Prometheus on port 9090
- Grafana on port 3000

## Step 3: Wait for Services to Initialize

Wait 1-2 minutes for all services to start. You can check status with:

```bash
docker-compose ps
```

All services should show "Up".

## Step 4: Access the Services

1. **API**: http://localhost:8000
   - Try the root endpoint: `curl http://localhost:8000`

2. **MLflow**: http://localhost:5000
   - View experiments and model runs

3. **Airflow**: http://localhost:8080
   - Default login: admin/admin
   - Enable and run the diabetes prediction pipeline

4. **Grafana**: http://localhost:3000
   - Default login: admin/admin
   - View monitoring dashboards

## Step 5: Make a Prediction

Try the prediction API:

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

## Step 6: Run the Complete Pipeline

1. Go to Airflow UI (http://localhost:8080)
2. Enable the "diabetes_prediction_pipeline" DAG
3. Trigger a manual run
4. Watch the pipeline execute all steps:
   - Data ingestion
   - Feature engineering
   - Model training
   - Model evaluation
   - Model registration

## Next Steps

- Customize the model training parameters
- Add new features to the feature store
- Extend the API with additional endpoints
- Configure alerts in Grafana
- Set up CI/CD with GitHub Actions

## Shutting Down

To stop all services:

```bash
docker-compose down
```

To stop and remove all data:

```bash
docker-compose down -v
```

## Need Help?

- Check the [full documentation](index.md)
- View service logs: `docker-compose logs <service-name>`
- Report issues on GitHub
