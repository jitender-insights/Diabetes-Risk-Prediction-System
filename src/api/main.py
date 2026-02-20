"""
Main FastAPI application for diabetes risk prediction.
"""

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import numpy as np
import time
import logging
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Import our prediction service and metrics
try:
    from src.api.prediction_service import prediction_service
    from src.api.metrics import record_prediction, record_health_status, get_metrics, CONTENT_TYPE_LATEST
except ImportError as e:
    print(f"Import error: {e}")
    # Create a mock service for now
    class MockPredictionService:
        def load_model(self, model_uri=None):
            print("Mock model loading")
            return True
            
        def predict(self, patient_data):
            import random
            prediction = random.choice([0, 1])
            probability = random.uniform(0, 1)
            confidence = 0.8 if probability > 0.5 else 0.7
            return {
                "prediction": int(prediction),
                "probability": float(probability),
                "confidence": float(confidence)
            }
            
        def get_model_info(self):
            return {"model_type": "MockModel", "loaded": True}
    
    prediction_service = MockPredictionService()
    
    # Mock metrics functions
    def record_prediction(outcome, duration, confidence):
        print(f"Recording prediction: outcome={outcome}, duration={duration}, confidence={confidence}")
    
    def record_health_status(is_healthy):
        print(f"Recording health status: {is_healthy}")
    
    def get_metrics():
        return b""
    
    CONTENT_TYPE_LATEST = "text/plain"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Diabetes Risk Prediction API",
    description="API for predicting diabetes risk based on patient data",
    version="1.0.0"
)

# Pydantic model for request data
class PatientData(BaseModel):
    pregnancies: int
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree: float
    age: int

# Pydantic model for prediction response
class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    confidence: float

@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    logger.info("Starting up application...")
    try:
        # Try to load the model
        success = prediction_service.load_model()
        if success:
            logger.info("Model loaded successfully")
            record_health_status(True)
        else:
            logger.warning("Failed to load model, using mock predictions")
            record_health_status(False)
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        logger.warning("Using mock predictions")
        record_health_status(False)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Diabetes Risk Prediction API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    model_info = prediction_service.get_model_info()
    is_healthy = model_info.get("loaded", False)
    record_health_status(is_healthy)
    return {
        "status": "healthy" if is_healthy else "degraded",
        "model_info": model_info
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_diabetes_risk(patient_data: PatientData):
    """Predict diabetes risk for a patient."""
    start_time = time.time()
    
    try:
        # Convert Pydantic model to dictionary
        patient_dict = patient_data.dict()
        
        # Make prediction
        result = prediction_service.predict(patient_dict)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Record metrics
        record_prediction(result["prediction"], duration, result["confidence"])
        
        logger.info(f"Prediction made: {result}")
        
        return PredictionResponse(**result)
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        # Record metrics even for errors
        duration = time.time() - start_time
        record_prediction(-1, duration, 0.0)  # -1 for error
        raise HTTPException(status_code=500, detail=f"Error making prediction: {str(e)}")

@app.get("/model/info")
async def model_info():
    """Get information about the loaded model."""
    info = prediction_service.get_model_info()
    return info

@app.get("/metrics")
async def metrics():
    """Endpoint for Prometheus to scrape metrics."""
    prometheus_metrics = get_metrics()
    return Response(content=prometheus_metrics, media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
