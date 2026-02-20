"""
Data processing pipeline for Diabetes Risk Prediction System.
Handles data validation, cleaning, and preprocessing.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiabetesDataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_columns = [
            'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
            'insulin', 'bmi', 'diabetes_pedigree', 'age'
        ]
        
    def load_data(self, filepath):
        """Load data from CSV file."""
        logger.info(f"Loading data from {filepath}")
        data = pd.read_csv(filepath)
        
        # Add timestamp columns required by Feast
        if 'date' not in data.columns:
            # Add a placeholder date column for Feast
            data['date'] = pd.Timestamp.now()
            
        if 'created' not in data.columns:
            # Add a created timestamp column
            data['created'] = pd.Timestamp.now()
            
        logger.info(f"Loaded {len(data)} records")
        return data
    
    def validate_data(self, data):
        """Validate data quality and consistency."""
        logger.info("Validating data quality")
        
        # Check for missing values
        missing_values = data.isnull().sum()
        if missing_values.any():
            logger.warning(f"Missing values detected:\n{missing_values[missing_values > 0]}")
            
        # Check for negative values in columns that shouldn't have them
        positive_columns = ['glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi']
        for col in positive_columns:
            if (data[col] < 0).any():
                logger.warning(f"Negative values found in {col}")
                
        # Check for zero values in columns that shouldn't have them
        zero_columns = ['glucose', 'blood_pressure', 'bmi']
        for col in zero_columns:
            zeros = (data[col] == 0).sum()
            if zeros > 0:
                logger.warning(f"{zeros} zero values found in {col}")
                
        return True
    
    def preprocess_data(self, data):
        """Clean and preprocess the data."""
        logger.info("Preprocessing data")
        
        # Replace zero values with NaN for certain columns
        zero_columns = ['glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi']
        data_processed = data.copy()
        
        for col in zero_columns:
            data_processed[col] = data_processed[col].replace(0, np.nan)
            
        # Handle missing values by imputing with median
        for col in zero_columns:
            median_val = data_processed[col].median()
            data_processed[col] = data_processed[col].fillna(median_val)
            logger.info(f"Filled missing values in {col} with median: {median_val}")
            
        return data_processed
    
    def prepare_features(self, data):
        """Prepare features for training."""
        logger.info("Preparing features")
        
        X = data[self.feature_columns]
        y = data['outcome']
        
        return X, y
    
    def scale_features(self, X_train, X_test=None, fit=True):
        """Scale features using StandardScaler."""
        if fit:
            logger.info("Fitting scaler and transforming features")
            X_train_scaled = self.scaler.fit_transform(X_train)
            if X_test is not None:
                X_test_scaled = self.scaler.transform(X_test)
                return X_train_scaled, X_test_scaled
            return X_train_scaled
        else:
            logger.info("Transforming features with fitted scaler")
            return self.scaler.transform(X_test)
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Split data into train and test sets."""
        logger.info(f"Splitting data with test size {test_size}")
        return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    
    def process_pipeline(self, filepath):
        """Complete data processing pipeline."""
        # Load data
        data = self.load_data(filepath)
        
        # Validate data
        self.validate_data(data)
        
        # Preprocess data
        data_processed = self.preprocess_data(data)
        
        # Prepare features
        X, y = self.prepare_features(data_processed)
        
        # Split data
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        
        # Scale features
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test, fit=True)
        
        logger.info("Data processing pipeline completed")
        return X_train_scaled, X_test_scaled, y_train, y_test

if __name__ == "__main__":
    # Example usage
    processor = DiabetesDataProcessor()
    X_train, X_test, y_train, y_test = processor.process_pipeline("../../data/diabetes_data.csv")
    
    logger.info(f"Training set size: {X_train.shape}")
    logger.info(f"Test set size: {X_test.shape}")
