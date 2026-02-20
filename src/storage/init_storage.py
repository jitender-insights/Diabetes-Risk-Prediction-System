"""
Initialize storage systems for Diabetes Prediction System.
"""

import psycopg2
import boto3
import os
from botocore.exceptions import ClientError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_postgres():
    """Initialize PostgreSQL database."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            database=os.getenv('POSTGRES_DB', 'postgres'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'postgres')
        )
        
        cursor = conn.cursor()
        
        # Create databases
        cursor.execute("CREATE DATABASE airflow_db")
        cursor.execute("CREATE DATABASE mlflow_db")
        
        # Create users
        cursor.execute("CREATE USER airflow_user WITH PASSWORD 'airflow_pass'")
        cursor.execute("CREATE USER mlflow_user WITH PASSWORD 'mlflow_pass'")
        
        # Grant privileges
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user")
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("PostgreSQL initialization completed")
        
    except Exception as e:
        logger.error(f"Error initializing PostgreSQL: {e}")

def init_minio():
    """Initialize MinIO storage."""
    try:
        # Create MinIO client
        s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv('MINIO_ENDPOINT', 'http://localhost:9000'),
            aws_access_key_id=os.getenv('MINIO_ROOT_USER', 'minioadmin'),
            aws_secret_access_key=os.getenv('MINIO_ROOT_PASSWORD', 'minioadmin'),
            region_name='us-east-1'
        )
        
        # Create buckets
        buckets = ['mlflow-artifacts', 'diabetes-data', 'model-registry']
        
        for bucket in buckets:
            try:
                s3_client.create_bucket(Bucket=bucket)
                logger.info(f"Created bucket: {bucket}")
            except ClientError as e:
                if e.response['Error']['Code'] == 'BucketAlreadyExists':
                    logger.info(f"Bucket already exists: {bucket}")
                else:
                    logger.error(f"Error creating bucket {bucket}: {e}")
        
        logger.info("MinIO initialization completed")
        
    except Exception as e:
        logger.error(f"Error initializing MinIO: {e}")

def main():
    """Main initialization function."""
    logger.info("Initializing storage systems...")
    
    # Initialize PostgreSQL
    init_postgres()
    
    # Initialize MinIO
    init_minio()
    
    logger.info("Storage systems initialization completed")

if __name__ == "__main__":
    main()
