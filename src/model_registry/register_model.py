"""
Register a trained model in the MLflow model registry.
"""

import mlflow
import os

def register_trained_model(run_id, model_name="diabetes-predictor"):
    """Register a model from a specific run."""
    # Construct model URI from run ID
    model_uri = f"runs:/{run_id}/model"
    
    try:
        # Register the model
        model_details = mlflow.register_model(model_uri, model_name)
        print(f"Model registered with name '{model_name}' and version {model_details.version}")
        return model_details
    except Exception as e:
        print(f"Error registering model: {e}")
        return None

def transition_to_production(model_name, version):
    """Transition a model version to Production stage."""
    try:
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage="Production"
        )
        print(f"Model {model_name} version {version} transitioned to Production")
    except Exception as e:
        print(f"Error transitioning model to Production: {e}")

def get_production_model_uri(model_name):
    """Get the URI of the production model."""
    try:
        client = mlflow.tracking.MlflowClient()
        latest_versions = client.get_latest_versions(model_name, stages=["Production"])
        
        if latest_versions:
            production_version = latest_versions[0]
            model_uri = f"models:/{model_name}/{production_version.version}"
            print(f"Production model URI: {model_uri}")
            return model_uri
        else:
            print("No production model found")
            return None
    except Exception as e:
        print(f"Error retrieving production model: {e}")
        return None

def list_registered_models():
    """List all registered models."""
    try:
        client = mlflow.tracking.MlflowClient()
        registered_models = client.list_registered_models()
        
        print("Registered models:")
        for model in registered_models:
            print(f" - {model.name}")
            
        return registered_models
    except Exception as e:
        print(f"Error listing registered models: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    print("Model registry utilities loaded")
    print("Available functions:")
    print(" - register_trained_model(run_id, model_name)")
    print(" - transition_to_production(model_name, version)")
    print(" - get_production_model_uri(model_name)")
    print(" - list_registered_models()")
