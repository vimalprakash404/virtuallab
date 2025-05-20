import json 
from database.schema import user_schema
from database.connection import client , database
import datetime


users_collection = database["users"]

# Insert sample data (optional)
sample_user_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "age": int(30),
    # Add more fields as needed
}
users_collection.insert_one(sample_user_data)

# Validate schema for the collection
def validate_schema(document, schema):
    for field, field_info in schema.items():
        field_type = field_info.get("type")
        field_required = field_info.get("required", False)

        if field_required and field not in document:
            raise ValueError(f"Field '{field}' is required but not found in the document.")

        field_value = document.get(field)

        if field_value is not None and field_type and not isinstance(field_value, type(None)) and not isinstance(field_value, type(field_type)):
            raise ValueError(f"Field '{field}' should be of type {field_type}.")

# Example of validating the schema for a document
try:
    validate_schema(sample_user_data, user_schema)
    print("Document schema is valid.")
except ValueError as e:
    print(f"Validation error: {e}")
