"""
Feature definitions for the diabetes prediction feature store.
"""

from datetime import timedelta
from feast import Entity, Feature, FeatureView, ValueType, FileSource
import os

# Define the entity (patient)
patient = Entity(
    name="patient",
    value_type=ValueType.INT64,
    description="Patient identifier"
)

# Define the data source
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_source = FileSource(
    path=os.path.join(project_dir, "data", "diabetes_data.csv"),
    event_timestamp_column="date",
    created_timestamp_column="created",
)

# Define feature views
patient_features_view = FeatureView(
    name="patient_features",
    entities=["patient"],
    ttl=timedelta(days=1),
    features=[
        Feature(name="pregnancies", dtype=ValueType.INT32),
        Feature(name="glucose", dtype=ValueType.INT32),
        Feature(name="blood_pressure", dtype=ValueType.INT32),
        Feature(name="skin_thickness", dtype=ValueType.INT32),
        Feature(name="insulin", dtype=ValueType.INT32),
        Feature(name="bmi", dtype=ValueType.FLOAT),
        Feature(name="diabetes_pedigree", dtype=ValueType.FLOAT),
        Feature(name="age", dtype=ValueType.INT32),
    ],
    online=True,
    input=data_source,
    tags={}
)
