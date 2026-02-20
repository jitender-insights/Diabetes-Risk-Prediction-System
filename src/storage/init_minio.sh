#!/bin/bash

# Initialize MinIO for Diabetes Prediction System

# Set environment variables
export MINIO_ROOT_USER=minioadmin
export MINIO_ROOT_PASSWORD=minioadmin

# Create buckets
mc alias set myminio http://minio:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
mc mb myminio/mlflow-artifacts
mc mb myminio/diabetes-data
mc mb myminio/model-registry

# Set bucket policies
mc anonymous set download myminio/mlflow-artifacts
mc anonymous set download myminio/diabetes-data
mc anonymous set none myminio/model-registry

echo "MinIO initialization completed"
