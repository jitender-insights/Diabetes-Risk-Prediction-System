"""
Initialize the Feast feature store repository.
"""

import os
import subprocess
import sys

def initialize_feast_repo():
    """
    Initialize the Feast feature repository.
    """
    # Change to the feature_store directory
    feature_store_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(feature_store_dir)
    
    print("Initializing Feast repository...")
    
    # In a real implementation, we would run:
    # feast init diabetes_feature_repo
    # But we'll create the structure manually instead
    
    # Create the directory structure
    repo_dir = "diabetes_feature_repo"
    if not os.path.exists(repo_dir):
        os.makedirs(os.path.join(repo_dir, "features"))
        print(f"Created directory structure in {repo_dir}")
    
    # Create a basic feature_store.yaml
    feature_store_yaml = f"""
project: diabetes_prediction
registry: data/registry.db
provider: local
online_store:
    path: data/online_store.db
"""
    
    with open(os.path.join(repo_dir, "feature_store.yaml"), "w") as f:
        f.write(feature_store_yaml.strip())
    
    print("Created feature_store.yaml")
    
    # Copy our feature definitions
    features_src = os.path.join("..", "feature_store", "features", "diabetes_features.py")
    features_dst = os.path.join(repo_dir, "features", "diabetes_features.py")
    
    if os.path.exists(features_src):
        with open(features_src, "r") as src_file:
            with open(features_dst, "w") as dst_file:
                dst_file.write(src_file.read())
        print("Copied feature definitions")
    
    print("Feast repository initialized!")

if __name__ == "__main__":
    initialize_feast_repo()
