-- Initialize PostgreSQL database for Diabetes Prediction System

-- Create database for Airflow
CREATE DATABASE airflow_db;

-- Create user for Airflow
CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;

-- Create database for MLflow
CREATE DATABASE mlflow_db;

-- Create user for MLflow
CREATE USER mlflow_user WITH PASSWORD 'mlflow_pass';
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;

-- Connect to airflow_db
\c airflow_db

-- Create tables for Airflow metadata (simplified)
CREATE TABLE IF NOT EXISTS experiment_metadata (
    id SERIAL PRIMARY KEY,
    experiment_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

CREATE TABLE IF NOT EXISTS model_deployment_log (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    environment VARCHAR(50) NOT NULL,
    deployed_by VARCHAR(255)
);

-- Connect to mlflow_db
\c mlflow_db

-- Create tables for MLflow tracking (simplified)
CREATE TABLE IF NOT EXISTS model_performance_log (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(255) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions
GRANT ALL PRIVILEGES ON TABLE experiment_metadata TO airflow_user;
GRANT ALL PRIVILEGES ON TABLE model_deployment_log TO airflow_user;
GRANT ALL PRIVILEGES ON TABLE model_performance_log TO mlflow_user;
