"""
Tests for the data processor module.
"""

import sys
import os
import pandas as pd
import numpy as np
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_pipeline.data_processor import DiabetesDataProcessor

def test_data_processor_initialization():
    """Test that the data processor initializes correctly."""
    processor = DiabetesDataProcessor()
    assert processor is not None
    assert hasattr(processor, 'scaler')

def test_load_data():
    """Test loading data from CSV."""
    processor = DiabetesDataProcessor()
    # Create a simple test dataframe
    test_data = pd.DataFrame({
        'pregnancies': [1, 2, 3],
        'glucose': [100, 110, 120],
        'blood_pressure': [70, 80, 90],
        'skin_thickness': [20, 25, 30],
        'insulin': [100, 110, 120],
        'bmi': [25.0, 26.0, 27.0],
        'diabetes_pedigree': [0.5, 0.6, 0.7],
        'age': [25, 30, 35],
        'outcome': [0, 1, 0]
    })
    
    # Save test data to temporary file
    temp_file = 'temp_test_data.csv'
    test_data.to_csv(temp_file, index=False)
    
    # Load data
    loaded_data = processor.load_data(temp_file)
    
    # Clean up
    os.remove(temp_file)
    
    # Assertions
    assert len(loaded_data) == 3
    assert list(loaded_data.columns) == list(test_data.columns)

def test_preprocess_data():
    """Test data preprocessing functionality."""
    processor = DiabetesDataProcessor()
    
    # Create test data with some zeros
    test_data = pd.DataFrame({
        'pregnancies': [1, 2, 3],
        'glucose': [100, 0, 120],  # zero value
        'blood_pressure': [70, 0, 90],  # zero value
        'skin_thickness': [20, 25, 30],
        'insulin': [100, 110, 120],
        'bmi': [25.0, 26.0, 0.0],  # zero value
        'diabetes_pedigree': [0.5, 0.6, 0.7],
        'age': [25, 30, 35],
        'outcome': [0, 1, 0]
    })
    
    processed_data = processor.preprocess_data(test_data)
    
    # Check that zeros were replaced with medians
    # Note: This assumes the median calculation replaces zeros appropriately
    assert (processed_data['glucose'] != 0).all() or (processed_data['glucose'] == 0).sum() < (test_data['glucose'] == 0).sum()

def test_prepare_features():
    """Test preparing features for training."""
    processor = DiabetesDataProcessor()
    
    # Create test data
    test_data = pd.DataFrame({
        'pregnancies': [1, 2, 3],
        'glucose': [100, 110, 120],
        'blood_pressure': [70, 80, 90],
        'skin_thickness': [20, 25, 30],
        'insulin': [100, 110, 120],
        'bmi': [25.0, 26.0, 27.0],
        'diabetes_pedigree': [0.5, 0.6, 0.7],
        'age': [25, 30, 35],
        'outcome': [0, 1, 0]
    })
    
    X, y = processor.prepare_features(test_data)
    
    # Assertions
    assert X.shape == (3, 8)  # 3 samples, 8 features
    assert y.shape == (3,)     # 3 target values
    assert list(X.columns) == processor.feature_columns
    assert y.name == 'outcome'
