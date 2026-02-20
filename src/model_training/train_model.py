"""
Train a diabetes prediction model using Scikit-learn and track with MLflow.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import mlflow
import mlflow.sklearn
import yaml
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiabetesModelTrainer:
    def __init__(self):
        self.model = None
        self.feature_names = [
            'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
            'insulin', 'bmi', 'diabetes_pedigree', 'age'
        ]
        
    def load_and_preprocess_data(self, data_path):
        """Load and preprocess data."""
        logger.info(f"Loading data from {data_path}")
        df = pd.read_csv(data_path)
        
        # Prepare features and target
        X = df[self.feature_names]
        y = df['outcome']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"Training set size: {X_train.shape}")
        logger.info(f"Test set size: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test
    
    def train_random_forest(self, X_train, y_train, params=None):
        """Train a Random Forest model."""
        if params is None:
            params = {
                'n_estimators': 100,
                'max_depth': 10,
                'random_state': 42
            }
            
        logger.info("Training Random Forest model")
        self.model = RandomForestClassifier(**params)
        self.model.fit(X_train, y_train)
        
        return self.model
    
    def train_logistic_regression(self, X_train, y_train, params=None):
        """Train a Logistic Regression model."""
        if params is None:
            params = {
                'C': 1.0,
                'random_state': 42
            }
            
        logger.info("Training Logistic Regression model")
        self.model = LogisticRegression(**params)
        self.model.fit(X_train, y_train)
        
        return self.model
    
    def hyperparameter_tuning(self, X_train, y_train, model_type='random_forest'):
        """Perform hyperparameter tuning."""
        logger.info(f"Performing hyperparameter tuning for {model_type}")
        
        if model_type == 'random_forest':
            model = RandomForestClassifier(random_state=42)
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10]
            }
        else:  # logistic_regression
            model = LogisticRegression(random_state=42)
            param_grid = {
                'C': [0.1, 1, 10, 100],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear']
            }
            
        # Perform grid search
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best cross-validation score: {grid_search.best_score_}")
        
        self.model = grid_search.best_estimator_
        return self.model, grid_search.best_params_, grid_search.best_score_
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate the trained model."""
        logger.info("Evaluating model")
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        logger.info(f"Accuracy: {accuracy:.4f}")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall: {recall:.4f}")
        logger.info(f"F1 Score: {f1:.4f}")
        
        # Detailed classification report
        report = classification_report(y_test, y_pred)
        logger.info(f"Classification Report:\n{report}")
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
    
    def log_to_mlflow(self, params, metrics, model_name="diabetes_model"):
        """Log model and metrics to MLflow."""
        logger.info("Logging to MLflow")
        
        with mlflow.start_run():
            # Log parameters
            for key, value in params.items():
                mlflow.log_param(key, value)
                
            # Log metrics
            for key, value in metrics.items():
                if key not in ['y_pred', 'y_pred_proba']:
                    mlflow.log_metric(key, value)
                    
            # Log model
            mlflow.sklearn.log_model(self.model, model_name)
            
            # Log feature importance if available
            if hasattr(self.model, 'feature_importances_'):
                feat_imp = dict(zip(self.feature_names, self.model.feature_importances_))
                mlflow.log_metrics(feat_imp)
                
            logger.info("Model logged to MLflow")

def main():
    """Main training function."""
    # Initialize trainer
    trainer = DiabetesModelTrainer()
    
    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(project_root, "data", "diabetes_data.csv")
    
    # Load and preprocess data
    X_train, X_test, y_train, y_test = trainer.load_and_preprocess_data(data_path)
    
    # Train model (example with Random Forest)
    model_params = {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42
    }
    
    trainer.train_random_forest(X_train, y_train, model_params)
    
    # Evaluate model
    metrics = trainer.evaluate_model(X_test, y_test)
    
    # Log to MLflow
    trainer.log_to_mlflow(model_params, metrics)
    
    logger.info("Model training completed successfully")

if __name__ == "__main__":
    main()
