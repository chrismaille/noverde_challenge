"""Noverde Policy Class."""
from dataclasses import dataclass, field
from typing import Dict, Union

import arrow
import requests
from loguru import logger

from noverde_challenge.models.loan import LoanModel
from noverde_challenge.policies.stakeholders import StakeholderBasePolicy
from noverde_challenge.utils.secrets import get_secret


@dataclass
class NoverdePolicy(StakeholderBasePolicy):
    """Noverde Policy Rules Class."""

    valid_terms = [6, 9, 12]
    minimum_age = 18
    minimum_amount = 1000.00
    maximum_amount = 4000.00
    minimum_score = 600

    loan: LoanModel

    request_base_url = "https://challenge.noverde.name/"
    request_timeout: int = 5

    policy_results: Dict[str, bool] = field(default_factory=dict)

    def request_score(self) -> int:
        """Request Score to External Service."""
        return self._request("score")  # type: ignore

    def request_commitment(self) -> float:
        """Request Commitment to External Service."""
        return self._request("commitment")  # type: ignore

    def _request(self, response_field: str) -> Union[str, int, float]:
        url = f"{self.request_base_url}{response_field}"
        logger.debug(f"Starting request for {url}. Timeout is {self.request_timeout}.")
        data = {"cpf": self.loan.cpf}
        headers = {
            "Content-Type": "application/json",
            "x-api-key": get_secret("/noverde/api/token"),
        }
        response = requests.post(
            url, data=data, headers=headers, timeout=self.request_timeout
        )
        response.raise_for_status()
        return response.json()[response_field]

    @classmethod
    def run_amount_policy(cls, amount: float) -> bool:
        """Run Amount Policy Rule.

        Current Rule:
            * Loan Minimum Value: 1000.0
            * Loan Maximum Value: 4000.0

        :param amount: loan value
        :return: Boolean
        """
        return cls.minimum_amount <= amount <= cls.maximum_amount

    def run_age_policy(self) -> bool:
        """Run Age Policy Rule.

        Current Rule:
            * Age equal or greater than 18 years

        :return: Boolean
        """
        days = (arrow.utcnow() - arrow.get(self.loan.birthdate)).days
        return (days / 365) >= self.minimum_age

    def run_score_policy(self) -> bool:
        """Run Score Policy Rule.

        Current Rule:
            * Score minimum: 600

        :return: Boolean
        """
        score = self.request_score()
        return score >= self.minimum_score

    def run_commitment_policy(self, pmt: float) -> bool:
        """Run Commitment Policy Rule.

        Current Rule:
            * Calculated PMT must be equal or
                less than commitment-free value (CFV)

        Example:
            Borrower Income: 1000.00
            Borrower commitment rate: 0.8
            Borrower commitment-free value: 1000 * (1 - 0.8) = 200.0
            PMT 150.00 <= CFV 200.00 -> True
            PMT 400.00 <= CFV 200.00 -> False

        :param pmt: calculated PMT for Borrower
        :return: Boolean
        """
        commitment_rate = self.request_commitment()
        commitment_free_value: float = self.loan.income * (1 - commitment_rate)
        return pmt <= commitment_free_value

    @classmethod
    def run_terms_policy(cls, value: int) -> bool:
        """Run Terms Policy Rule.

        Current Rule:
            * Valid Terms: 6, 9 or 12 months

        :param value: proposed term
        :return: Boolean
        """
        return value in cls.valid_terms
