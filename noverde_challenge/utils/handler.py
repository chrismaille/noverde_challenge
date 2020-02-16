"""Handler Config Decorator."""
import json
from functools import wraps
from typing import Optional, Type

from loguru import logger
from marshmallow import Schema, ValidationError
from sentry_sdk import capture_exception  # type: ignore

from noverde_challenge.utils.status_code import StatusCode


def handler_view(model_schema: Optional[Type[Schema]] = None):
    """Configure Handler Decorator.

    This decorator will config the handler for the following options:

        * model_schema: The Marshmallow schema to be used in POST requests


    Think this decorator a very simple middleware for handlers. Current workflow is:

        1. Get json data from event["body"]
        2. Deserialize data using Marshmallow
        3. Save data on DynamoDB
        4. Invoke the Handler function
        5. Return Handler data, in a compatible API Gateway response
        6. Handle Errors

    :param model_schema: Marshmallow Schema
    :return: Dict
    """

    def config(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # Get Body data
                event = args[0]
                body = event.get("body")
                raw_data = json.loads(body) if body else None

                # Create Loan object
                if raw_data and model_schema:
                    logger.debug("Start creating loan...")
                    loan = model_schema().load(raw_data)
                    kwargs["loan"] = loan

                # Call Handler
                ret = f(*args, **kwargs)

                # Return API Gateway compatible data
                return {
                    "statusCode": ret["statusCode"].value,
                    "body": json.dumps(ret["body"]),
                }
            except ValidationError as error:
                # Handle Bad Request Errors
                logger.error(f"Validation Error during request: {error.messages}")
                error_list = [
                    f"{field_key}: {description}"
                    for field_key in error.messages
                    for description in error.messages[field_key]
                ]
                return {
                    "statusCode": StatusCode.BAD_REQUEST.value,
                    "body": json.dumps({"errors": error_list}),
                }
            except Exception as error:
                # Handle Internal Server Errors
                capture_exception(error)
                logger.error(f"Internal Error during request: {error}")
                return {
                    "statusCode": StatusCode.INTERNAL_ERROR.value,
                    "body": json.dumps({"error": [str(error)]}),
                }

        return wrapper

    return config
