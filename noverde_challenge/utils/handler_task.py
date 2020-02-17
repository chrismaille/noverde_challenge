"""Handler Task Config Decorator."""
from functools import wraps

from loguru import logger
from sentry_sdk import capture_exception  # type: ignore

from noverde_challenge.models.loan import (
    LoanAnalysisResult,
    LoanAnalysisStatus,
    LoanModel,
    LoanRefusedPolicy,
)
from noverde_challenge.policies.stakeholders.noverde import NoverdePolicy


def handler_task(refused_policy: LoanRefusedPolicy):
    """Configure Handler Task Decorator.

    This decorator will config the handler for the following options:

        * refused_policy: The Policy which will be used on refused analysis


    Workflow:

        1. Get Input data
        2. Find Loan and Policy Class
        3. Invoke the Handler function
        5. Save refused policy in database, if any.
        6. Handle Errors

    :param refused_policy: LoanRefusedPolicy enum
    :return: Dict
    """

    def config(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                logger.debug(args)
                logger.debug(kwargs)

                # Get input data
                event = args[0]
                loan_id = event.get("loan_id")

                # Get Loan object
                loan = LoanModel.get(hash_key=loan_id)
                kwargs["loan"] = loan

                # Get Stakeholder Policy
                # For this challenge, it will be fixed
                policy_class = NoverdePolicy
                kwargs["policy_class"] = policy_class

                # Call Handler
                result: bool = f(*args, **kwargs)

                # Mark loan refused
                if not result:
                    loan.status = LoanAnalysisStatus.COMPLETED.value
                    loan.refused_policy = refused_policy.value
                    loan.result = LoanAnalysisResult.REFUSED.value
                    loan.save()
                    logger.info(f"[{loan.loan_id}] Loan is DENIED")

                # Return data
                return {
                    "loan_id": loan.loan_id,
                    "status": loan.status,
                    "result": loan.result,
                }
            except Exception as error:
                # For this challenge, error handling will be very simple.
                # In production settings, some errors are handled here
                # and others are handled in State Machine,
                # to allow Catch, Retry, etc.. (ex. Timeouts)
                capture_exception(error)
                logger.error(f"Internal Error during request: {error}")
                raise

        return wrapper

    return config
