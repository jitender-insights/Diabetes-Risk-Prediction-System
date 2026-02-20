"""
Airflow DAG for the Diabetes Risk Prediction Pipeline.
This DAG orchestrates the entire MLOps pipeline from data ingestion to model deployment.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

# Import our modules
try:
    from src.data_pipeline.data_processor import DiabetesDataProcessor
    from src.model_training.train_model import DiabetesModelTrainer
    from src.model_registry.register_model import register_trained_model
except ImportError as e:
    print(f"Import error: {e}")
    # We'll define dummy functions for now
    def dummy_function(**kwargs):
        print("Dummy function executed")

# Default arguments for the DAG
default_args = {
    'owner': 'mlops-team',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'diabetes_prediction_pipeline',
    default_args=default_args,
    description='MLOps pipeline for diabetes risk prediction',
    schedule_interval=timedelta(days=1),  # Run daily
    catchup=False,
    tags=['mlops', 'diabetes', 'healthcare'],
)

def data_ingestion_task(**kwargs):
    """Task to ingest and validate data."""
    print("Ingesting and validating data...")
    # In a real implementation, this would:
    # 1. Download data from source
    # 2. Validate data quality
    # 3. Log data quality metrics
    print("Data ingestion completed.")
    return "Data ingestion successful"

def data_preprocessing_task(**kwargs):
    """Task to preprocess data."""
    print("Preprocessing data...")
    # In a real implementation, this would:
    # 1. Clean the data
    # 2. Handle missing values
    # 3. Normalize/scale features
    # 4. Split data into train/test sets
    print("Data preprocessing completed.")
    return "Data preprocessing successful"

def feature_engineering_task(**kwargs):
    """Task to engineer features."""
    print("Engineering features...")
    # In a real implementation, this would:
    # 1. Create new features
    # 2. Transform existing features
    # 3. Store features in feature store
    print("Feature engineering completed.")
    return "Feature engineering successful"

def model_training_task(**kwargs):
    """Task to train the model."""
    print("Training model...")
    # In a real implementation, this would:
    # 1. Load preprocessed data
    # 2. Train model
    # 3. Perform hyperparameter tuning
    # 4. Evaluate model
    # 5. Log results to MLflow
    print("Model training completed.")
    return "model_run_id_12345"  # Mock run ID

def model_validation_task(**kwargs):
    """Task to validate the trained model."""
    print("Validating model...")
    # In a real implementation, this would:
    # 1. Load trained model
    # 2. Run validation checks
    # 3. Compare with baseline model
    # 4. Determine if model meets performance criteria
    print("Model validation completed.")
    return "Model validation successful"

def model_registration_task(**kwargs):
    """Task to register the model in the registry."""
    print("Registering model...")
    ti = kwargs['ti']
    run_id = ti.xcom_pull(task_ids='train_model')
    if run_id:
        print(f"Registering model from run {run_id}")
        # In a real implementation, this would:
        # 1. Register model in MLflow registry
        # 2. Transition to staging/production based on validation
        print("Model registration completed.")
    else:
        print("No run ID found for model registration")
    return "Model registration successful"

# Define tasks
start_pipeline = DummyOperator(
    task_id='start_pipeline',
    dag=dag,
)

data_ingestion = PythonOperator(
    task_id='data_ingestion',
    python_callable=data_ingestion_task,
    dag=dag,
)

data_preprocessing = PythonOperator(
    task_id='data_preprocessing',
    python_callable=data_preprocessing_task,
    dag=dag,
)

feature_engineering = PythonOperator(
    task_id='feature_engineering',
    python_callable=feature_engineering_task,
    dag=dag,
)

model_training = PythonOperator(
    task_id='train_model',
    python_callable=model_training_task,
    dag=dag,
)

model_validation = PythonOperator(
    task_id='validate_model',
    python_callable=model_validation_task,
    dag=dag,
)

model_registration = PythonOperator(
    task_id='register_model',
    python_callable=model_registration_task,
    dag=dag,
)

end_pipeline = DummyOperator(
    task_id='end_pipeline',
    dag=dag,
)

# Set task dependencies
start_pipeline >> data_ingestion >> data_preprocessing >> feature_engineering >> model_training >> model_validation >> model_registration >> end_pipeline
