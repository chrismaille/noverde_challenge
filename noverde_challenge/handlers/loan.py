"""Hello Handlers."""
import json
from typing import Any, Dict

from loguru import logger
from pynamodb.exceptions import DoesNotExist

from noverde_challenge.models.loan import LoanModel
from noverde_challenge.schemas.loan import CreateLoanModelSchema, LoanModelSchema
from noverde_challenge.utils.handler import handler_view
from noverde_challenge.utils.status_code import StatusCode


@handler_view()
def get(event: Dict[str, Any], context: object) -> Dict[str, object]:
    """Loan Get Handler.

    :param loan: Loan Model instance
    :param event: Serverless Event instance
    :param context: Serverless Context instance
    :return: Dict
    """
    loan_id = event["pathParameters"]["loan_id"]
    logger.info(f"Start Retrieve Loan handler for id {loan_id}")
    try:
        loan = LoanModel.get(hash_key=loan_id)
    except DoesNotExist:
        return {
            "statusCode": StatusCode.NOT_FOUND,
            "body": {"errors": [f"LoanId {loan_id} does not found."]},
        }

    loan_response = json.loads(LoanModelSchema().dumps(loan))
    response = {"statusCode": StatusCode.OK, "body": loan_response}

    return response


@handler_view(model_schema=CreateLoanModelSchema)
def post(event: Dict[str, Any], context: object, loan: LoanModel) -> Dict[str, object]:
    """Loan Post Handler.

    :param event: Serverless Event Instance
    :param context: Serverless Context instance
    :param loan: Loan Model instance
    :return: Dict
    """
    logger.info(f"Starting Create Loan handler...")
    body = {"id": loan.loan_id}
    return {"statusCode": StatusCode.CREATED, "body": body}
