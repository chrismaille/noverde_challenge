"""Loan Model Module."""
import os
from enum import Enum, unique

from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model


@unique
class LoanStatus(Enum):
    """Loan Status."""

    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "ERROR"


@unique
class LoanAnalysisStatus(Enum):
    """Loan Analysis Status."""

    APPROVED = "approved"
    REFUSED = "refused"


class LoanModel(Model):
    """Loan Model.

    Attributes
        * loan_id (uuid): Loan hash key
        * cpf (string): Borrower CPF (range key)
        * birthdate (string): Borrower Birthday
        * amount (number): Loan value
        * terms (number): Loan instalments value
        * income (number): Borrower income
        * name (string): Borrower name

    """

    loan_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    cpf = UnicodeAttribute()
    birthdate = UnicodeAttribute()
    amount = NumberAttribute()
    terms = NumberAttribute()
    income = NumberAttribute()

    status = UnicodeAttribute(default=LoanStatus.PROCESSING.value)
    result = UnicodeAttribute(null=True)
    refused_policy = UnicodeAttribute(null=True)
    allowed_amount = NumberAttribute(null=True)
    allowed_terms = NumberAttribute(null=True)

    class Meta:
        """Schema Meta class."""

        table_name = os.getenv("DYNAMODB_TABLE")
