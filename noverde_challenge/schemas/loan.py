"""LoanModel Request Schemas."""
import os
import uuid
from parser import ParserError
from typing import Type

import arrow
from loguru import logger
from marshmallow import Schema, ValidationError, fields, post_load, validates
from validate_docbr import CPF

from noverde_challenge.models.loan import LoanModel
from noverde_challenge.policies.stakeholders import StakeholderBasePolicy
from noverde_challenge.policies.stakeholders.noverde import NoverdePolicy
from noverde_challenge.utils.helpers import only_numbers


class LoanModelSchema(Schema):
    """Loan Model Schema.

    This class represent the DTO linking the
    data between API requests and backend Storage.
    For this challenge, API requests will be from AWS API Gateway
    and backend storage will be from AWS DynamoDB.

    """

    def __init__(  # type: ignore
        self, policy_class: Type[StakeholderBasePolicy] = NoverdePolicy, *args, **kwargs
    ):
        """Initialize Class.

        For this challenge Select Stackholder strategy will be fixed.

        :param policy_class: StakeholderBasePolicy class
        :param args: Original Args
        :param kwargs: Original Key Args
        """
        self.policy_class = policy_class
        super().__init__(*args, **kwargs)

    loan_id = fields.UUID(missing=uuid.uuid4)
    name = fields.String(required=True)
    cpf = fields.String(required=True)
    birthdate = fields.String(required=True)
    amount = fields.Float(required=True)
    terms = fields.Integer(required=True)
    income = fields.Float(required=True)

    @validates("cpf")
    def validate_cpf(self, value: str) -> None:
        """Validate CPF number.

        :param value: cpf value from request.
        :return: None
        """
        cpf = CPF()
        if not cpf.validate(value):
            raise ValidationError("Invalid CPF number.")

    @validates("amount")
    def validate_amount(self, value: float) -> None:
        """Validate Amount from API request.

        :param value: amount value from request.
        :return: None
        :raises: Marshmallow ValidationError
        """
        if not self.policy_class.run_amount_policy(value):
            raise ValidationError(
                f"Amount must be between {self.policy_class.minimum_amount} "
                f"and {self.policy_class.maximum_amount}. "
                f"Current: {value}"
            )

    @validates("terms")
    def validate_terms(self, value: int) -> None:
        """Validate Terms from API request.

        :param value: terms value from request.
        :return: None
        :raises: Marshmallow ValidationError
        """
        if not self.policy_class.run_terms_policy(value):
            raise ValidationError(
                f"Terms must be one of {self.policy_class.valid_terms}."
            )

    @validates("birthdate")
    def validate_birthdate(self, value: str) -> None:
        """Validate Birthdate from API request.

        :param value: brithdate value from request.
        :return: None
        :raises: Marshmallow ValidationError
        """
        try:
            date = arrow.get(value, "YYYY-MM-DD")
            if date >= arrow.utcnow():
                raise ValidationError("Date must be lower than today")
        except ParserError:
            raise ValidationError("Date must be in format YYYY-MM-DD")


class CreateLoanModelSchema(LoanModelSchema):
    """Create Loan Model Schema."""

    @post_load
    def create_loan(self, data: dict, *args, **kwargs) -> LoanModel:  # type: ignore
        """Create Loan Model from deserialized data."""
        table_name = os.getenv("DYNAMODB_TABLE")
        logger.debug(f"Using table {table_name}")
        if not LoanModel.exists():
            LoanModel.create_table(
                read_capacity_units=1, write_capacity_units=1, wait=True
            )
        data["loan_id"] = data["loan_id"].hex
        data["cpf"] = only_numbers(data["cpf"])
        loan = LoanModel(**data)
        loan.save()
        return loan
