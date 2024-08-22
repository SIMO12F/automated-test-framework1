from jsonschema import validate
from src.logger import logger

def validate_schema(instance, schema):
    try:
        validate(instance=instance, schema=schema)
        logger.info("Schema validation passed")
        return True
    except jsonschema.exceptions.ValidationError as ve:
        logger.error(f"Schema validation failed: {ve}")
        return False

# Usage in tests:
# user_schema = {
#     "type": "object",
#     "properties": {
#         "id": {"type": "integer"},
#         "name": {"type": "string"},
#         "email": {"type": "string", "format": "email"}
#     },
#     "required": ["id", "name", "email"]
# }
# assert validate_schema(response.json(), user_schema), "Response does not match expected schema"