"""Stakeholder Policy Base Class."""
from abc import ABC, abstractmethod
from typing import Any, List

import numpy as np
import numpy_financial as npf
import pandas
from loguru import logger

from noverde_challenge.models.loan import LoanModel


class StakeholderBasePolicy(ABC):
    """Abstract Class for Stakeholder Policies.

    This class represents all Stakeholder rules and
    policies to effecting release the Loan.

    In some scenarios, stakeholder is informed
    together with Loan data (ex. Whitelabel scenarios)

    On another scenario, the stakeholder is selected based on
    running his policies against a Loan proposal.

    For this challenge, Stakeholder will be fixed
    for all Loans.

    """

    valid_terms: List[int]
    minimum_age: int
    minimum_amount: float
    maximum_amount: float
    minimum_score: int
    loan: LoanModel

    @classmethod
    @abstractmethod
    def run_amount_policy(cls, amount: float) -> bool:
        """Run Amount Policy as per Stakeholder rules."""
        pass

    @abstractmethod
    def run_age_policy(self) -> bool:
        """Run Age Policy as per Stakeholder rules."""
        pass

    @abstractmethod
    def run_score_policy(self) -> bool:
        """Run Score Policy as per Stakeholder rules."""
        pass

    @abstractmethod
    def run_commitment_policy(self) -> bool:
        """Run Commitment Policy as per Stakeholder rules."""
        pass

    @staticmethod
    def calculate_pmt(
        present_value: float, rate_interest: float, number_period: int
    ) -> Any:
        """Calculate PMT.

        Using Numpy library as per:
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.pmt.html

        For simplicity we will return float here. On production settings
        its safer to work with Decimal() instances.

        :param present_value: Loan Proposed Value
        :param rate_interest: Monthly Rate Interest
        :param number_period: Loan Instalments
        :return: float
        """
        logger.info(
            f"Calculating PMT Using: "
            f"Present Value: {present_value}, "
            f"Terms: {number_period}, Interest Rate: {rate_interest}"
        )
        pmt = npf.pmt(rate=rate_interest, nper=number_period, pv=present_value)
        pmt = np.round(pmt, decimals=2) * -1
        logger.debug(f"PMT is {pmt}")
        return pmt

    @classmethod
    @abstractmethod
    def run_terms_policy(cls, value: int) -> bool:
        """Run Terms Policy as per Stakeholder rules."""
        pass

    @abstractmethod
    def get_available_rates(self, score: int, min_term: int) -> pandas.Series:
        """Get Available Rates as per Stakeholder rules."""
        pass
