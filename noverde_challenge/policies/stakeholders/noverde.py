"""Noverde Policy Class."""
from dataclasses import dataclass, field
from typing import Dict, Union

import arrow
import numpy as np
import pandas
import requests
from loguru import logger

from noverde_challenge.models.loan import (
    LoanAnalysisResult,
    LoanAnalysisStatus,
    LoanModel,
)
from noverde_challenge.policies.stakeholders import StakeholderBasePolicy
from noverde_challenge.utils.rates import get_rates
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
        logger.debug(
            f"[{self.loan.loan_id}] Starting request for {url}. "
            f"Timeout is {self.request_timeout}."
        )
        data = {"cpf": self.loan.cpf}
        headers = {
            "Content-Type": "application/json",
            "x-api-key": get_secret("/noverde/api/token"),
        }
        response = requests.post(
            url, json=data, headers=headers, timeout=self.request_timeout
        )
        response.raise_for_status()
        logger.debug(f"[{self.loan.loan_id}] HTTP Response is: {response.text}")
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
        current_age = int(days / 365)
        result = current_age >= self.minimum_age
        logger.debug(
            f"[{self.loan.loan_id}] Testing Age Policy: "
            f"{current_age} >= {self.minimum_age} = {result}"
        )
        return result

    def run_score_policy(self) -> bool:
        """Run Score Policy Rule.

        Current Rule:
            * Score minimum: 600

        :return: Boolean
        """
        score = self.request_score()
        result = score >= self.minimum_score
        logger.debug(
            f"[{self.loan.loan_id}] Testing Score Policy: "
            f"{score} >= {self.minimum_score} = {result}"
        )
        return result

    def run_commitment_policy(self) -> bool:
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

        :return: Boolean
        """
        # Get Commitment
        commitment_rate = self.request_commitment()
        logger.debug(f"Borrower commitment rate is {commitment_rate}")

        # Get Score
        borrower_score = self.request_score()
        logger.debug(f"Borrower score is {borrower_score}")

        # Get CFV
        logger.debug(
            f"Calculating CFV using: Income: {self.loan.income}, "
            f"Commitment Rate: {commitment_rate}"
        )
        commitment_free_value: float = np.round(
            self.loan.income * (1 - commitment_rate), decimals=2
        )
        logger.debug(f"CFV is {commitment_free_value}")

        # Get Available Rates
        available_rates = self.get_available_rates(borrower_score, int(self.loan.terms))
        verbose_rates = [
            f"Term: {term}, Rate: {available_rates[term]}"
            for term in available_rates.keys()
        ]
        logger.info(f"Available rates are: {verbose_rates}")

        result = False
        for number_period in available_rates.keys():
            # Calculate PMT
            present_value = self.loan.amount
            rate_interest = available_rates[number_period]
            pmt = self.calculate_pmt(present_value, rate_interest, int(number_period))

            # Test Policy
            result = pmt <= commitment_free_value
            logger.debug(
                f"[{self.loan.loan_id}] Testing Commitment Policy: "
                f"PMT {pmt} <= CFV {commitment_free_value} = {result}"
            )

            # Update Loan if approved
            if result:
                self.loan.allowed_amount = pmt
                self.loan.allowed_terms = int(number_period)
                self.loan.status = LoanAnalysisStatus.COMPLETED.value
                self.loan.result = LoanAnalysisResult.APPROVED.value
                self.loan.save()
                logger.info(f"[{self.loan.loan_id}] is APPROVED")
                break

        return result

    @classmethod
    def run_terms_policy(cls, value: int) -> bool:
        """Run Terms Policy Rule.

        Current Rule:
            * Valid Terms: 6, 9 or 12 months

        :param value: proposed term
        :return: Boolean
        """
        return value in cls.valid_terms

    def get_available_rates(self, score: int, min_term: int) -> pandas.Series:
        """Get Current Available Rates.

        Current Rate Model can retrieved from
        CSV files in S3 buckets, State Machine requests,
        API requests, Database, etc...

        For this challenge, we will use a local CSV file.

        :param score: Borrower score
        :param min_term: Borrower selected term
        :return: Series
        """
        return get_rates(
            score=score,
            min_term=min_term,
            valid_terms=self.valid_terms,
            csv="noverde_rate_model",
        )
