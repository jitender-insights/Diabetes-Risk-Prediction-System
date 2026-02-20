"""
Prediction service for loading and using trained models.
"""

import mlflow
import mlflow.pyfunc
import pandas as pd
import numpy as np
import joblib
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiabetesPredictionService:
    def __init__(self):
        self.model = None
        self.feature_names = [
            'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
            'insulin', 'bmi', 'diabetes_pedigree', 'age'
        ]
        self.scaler = None
        
    def load_model(self, model_uri=None):
        """Load the trained model from MLflow."""
        try:
            if model_uri is None:
                # Try to load the production model
                model_uri = "models:/diabetes-predictor/Production"
            
            logger.info(f"Loading model from {model_uri}")
            self.model = mlflow.pyfunc.load_model(model_uri)
            logger.info("Model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading model from {model_uri}: {e}")
            # Fallback to loading a local model if available
            return self._load_local_model()
    
    def _load_local_model(self):
        """Load a local model as fallback."""
        try:
            # Try to load from local models directory
            local_model_path = os.path.join("models", "diabetes_model")
            if os.path.exists(local_model_path):
                self.model = joblib.load(local_model_path)
                logger.info("Loaded local model successfully")
                return True
            else:
                logger.warning("No local model found")
                return False
        except Exception as e:
            logger.error(f"Error loading local model: {e}")
            return False
    
    def predict(self, patient_data):
        """Make a prediction for patient data."""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        try:
            # Create DataFrame from patient data
            df = pd.DataFrame([patient_data])
            
            # Make prediction
            prediction = self.model.predict(df)[0]
            
            # Get probability if available
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(df)[0]
                probability = probabilities[1] if len(probabilities) > 1 else probabilities[0]
            else:
                probability = float(prediction)
            
            # Calculate confidence (simplified)
            confidence = 0.9 if probability > 0.7 else (0.7 if probability > 0.5 else 0.5)
            
            return {
                "prediction": int(prediction),
                "probability": float(probability),
                "confidence": float(confidence)
            }
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            raise
    
    def get_model_info(self):
        """Get information about the loaded model."""
        if self.model is None:
            return {"error": "Model not loaded"}
        
        # Try to get model metadata
        try:
            return {
                "model_type": type(self.model).__name__,
                "features": self.feature_names,
                "loaded": True
            }
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {"error": str(e)}

# Create a global instance
prediction_service = DiabetesPredictionService()
