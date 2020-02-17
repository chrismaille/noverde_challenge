"""Loan Analysis State Machine Handlers."""
from typing import Any, Dict, Type, Union

from loguru import logger

from noverde_challenge.models.loan import LoanModel, LoanRefusedPolicy
from noverde_challenge.policies.stakeholders import StakeholderBasePolicy
from noverde_challenge.policies.stakeholders.noverde import NoverdePolicy
from noverde_challenge.utils.handler_task import handler_task


@handler_task(refused_policy=LoanRefusedPolicy.AGE)
def run_age_policy(
    event: Dict[str, Any],
    context: object,
    loan: LoanModel,
    policy_class: Union[Type[NoverdePolicy], Type[StakeholderBasePolicy]],
) -> bool:
    """Run Age Policy Handler.

    :param event: Serverless event instance
    :param context: Serverless context instance
    :param loan: Loan Model instance
    :param policy_class: StakeholderBasePolicy subclass
    :return: bool
    """
    logger.info(f"Start Run Age Policy for {loan.loan_id}")
    return policy_class(loan=loan).run_age_policy()  # type: ignore


@handler_task(refused_policy=LoanRefusedPolicy.SCORE)
def run_score_policy(
    event: Dict[str, Any],
    context: object,
    loan: LoanModel,
    policy_class: Union[Type[NoverdePolicy], Type[StakeholderBasePolicy]],
) -> bool:
    """Run Score Policy Handler.

    :param event: Serverless event instance
    :param context: Serverless context instance
    :param loan: Loan Model instance
    :param policy_class: StakeholderBasePolicy subclass
    :return: bool
    """
    logger.info(f"Start Run Score Policy for {loan.loan_id}")
    return policy_class(loan=loan).run_score_policy()  # type: ignore


@handler_task(refused_policy=LoanRefusedPolicy.COMMITMENT)
def run_commitment_policy(
    event: Dict[str, Any],
    context: object,
    loan: LoanModel,
    policy_class: Union[Type[NoverdePolicy], Type[StakeholderBasePolicy]],
) -> bool:
    """Run Commitment Policy Handler.

    :param event: Serverless event instance
    :param context: Serverless context instance
    :param loan: Loan Model instance
    :param policy_class: StakeholderBasePolicy subclass
    :return: bool
    """
    logger.info(f"Start Run Commitment Policy for {loan.loan_id}")
    return False
