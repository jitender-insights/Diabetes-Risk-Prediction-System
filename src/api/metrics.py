"""
Metrics collection for the diabetes prediction API.
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_async import aio
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define metrics
prediction_counter = Counter(
    'diabetes_predictions_total',
    'Total number of diabetes predictions made',
    ['outcome']
)

prediction_duration_histogram = Histogram(
    'diabetes_prediction_duration_seconds',
    'Time spent processing diabetes predictions'
)

model_confidence_gauge = Gauge(
    'diabetes_model_confidence',
    'Current model confidence level'
)

api_health_status = Gauge(
    'diabetes_api_health_status',
    'Health status of the API (1 = healthy, 0 = unhealthy)'
)

# Initialize health status
api_health_status.set(1)  # Start as healthy

def record_prediction(outcome, duration, confidence):
    """Record metrics for a prediction."""
    try:
        prediction_counter.labels(outcome=str(outcome)).inc()
        prediction_duration_histogram.observe(duration)
        model_confidence_gauge.set(confidence)
        logger.info(f"Recorded prediction metrics: outcome={outcome}, duration={duration:.4f}s, confidence={confidence}")
    except Exception as e:
        logger.error(f"Error recording metrics: {e}")

def record_health_status(is_healthy):
    """Record the health status of the API."""
    try:
        status_value = 1 if is_healthy else 0
        api_health_status.set(status_value)
        logger.info(f"Recorded health status: {'healthy' if is_healthy else 'unhealthy'}")
    except Exception as e:
        logger.error(f"Error recording health status: {e}")

def get_metrics():
    """Get the latest metrics."""
    try:
        return generate_latest()
    except Exception as e:
        logger.error(f"Error generating metrics: {e}")
        return b""
