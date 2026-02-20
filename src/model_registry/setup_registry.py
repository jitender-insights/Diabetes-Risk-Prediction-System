"""
Set up MLflow model registry for diabetes prediction models.
"""

import mlflow
import os

def setup_mlflow_tracking():
    """Set up MLflow tracking configuration."""
    # Set tracking URI (using local filesystem for simplicity)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    mlflow.set_tracking_uri(f"file:///{os.path.join(project_root, 'mlruns').replace(os.sep, '/')}")
    
    print(f"MLflow tracking URI set to: {mlflow.get_tracking_uri()}")

def setup_model_registry():
    """Set up model registry for diabetes prediction."""
    # Create experiment if it doesn't exist
    experiment_name = "diabetes_prediction"
    
    try:
        exp_id = mlflow.create_experiment(experiment_name)
        print(f"Created experiment '{experiment_name}' with ID: {exp_id}")
    except Exception as e:
        print(f"Experiment '{experiment_name}' might already exist: {e}")
        exp_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        print(f"Using existing experiment ID: {exp_id}")
    
    # Set the experiment
    mlflow.set_experiment(experiment_name)
    print(f"Set experiment to '{experiment_name}'")

def register_model(model_uri, model_name="diabetes-predictor"):
    """Register a model in the MLflow model registry."""
    try:
        model_details = mlflow.register_model(model_uri, model_name)
        print(f"Model registered with name '{model_name}' and version {model_details.version}")
        return model_details
    except Exception as e:
        print(f"Error registering model: {e}")
        return None

def transition_model_stage(model_name, version, stage):
    """Transition a model to a specific stage (Staging, Production, Archived)."""
    try:
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )
        print(f"Model {model_name} version {version} transitioned to {stage}")
    except Exception as e:
        print(f"Error transitioning model stage: {e}")

def main():
    """Main setup function."""
    print("Setting up MLflow model registry...")
    
    # Set up tracking
    setup_mlflow_tracking()
    
    # Set up registry
    setup_model_registry()
    
    print("MLflow model registry setup completed!")

if __name__ == "__main__":
    main()
