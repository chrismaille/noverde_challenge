"""Hello Handler."""
import json
from typing import Dict, Union


def hello(
    event: Dict[str, Union[str, int, object]], context: object
) -> Dict[str, object]:
    """Hello World Handler.

    :param event: Serverless Event instance
    :param context: Serverless Context instance
    :return: Dict
    """
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
