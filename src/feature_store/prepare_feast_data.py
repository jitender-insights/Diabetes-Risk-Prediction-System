"""
Prepare data for Feast feature store.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def prepare_feature_data(input_file, output_file):
    """
    Prepare data for Feast by ensuring it has the required timestamp columns.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file with timestamp columns
    """
    print(f"Loading data from {input_file}")
    df = pd.read_csv(input_file)
    
    # Add required timestamp columns for Feast
    df['event_timestamp'] = datetime.now()
    df['created_timestamp'] = datetime.now()
    
    # In a real scenario, these would represent when the record was created
    # For demonstration, we'll just use the current timestamp
    
    print(f"Saving prepared data to {output_file}")
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} records")
    
    return df

if __name__ == "__main__":
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Prepare the data
    input_file = os.path.join(project_root, "data", "diabetes_data.csv")
    output_file = os.path.join(project_root, "data", "diabetes_data_with_timestamps.csv")
    
    prepare_feature_data(input_file, output_file)
