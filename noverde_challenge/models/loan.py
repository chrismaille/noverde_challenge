"""Loan Model Module.

For this challenge, we will use a
DynamoDb table with a very simple organization.

For production settings please check:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html

"""
import os
from enum import Enum, unique

from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model


@unique
class LoanAnalysisStatus(Enum):
    """Loan Analysis Status."""

    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "ERROR"


@unique
class LoanAnalysisResult(Enum):
    """Loan Analysis Result."""

    APPROVED = "approved"
    REFUSED = "refused"


@unique
class LoanRefusedPolicy(Enum):
    """Loan Refused Policy."""

    AGE = "age"
    SCORE = "score"
    COMMITMENT = "commitment"


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

        * status (LoanAnalysisStatus): Loan Analysis status
        * result (LoanAnalysisResult): Loan Analysis result
        * refused_policy (LoanRefusedPolicy): Loan Refused Policy
        * allowed_amount (number): allowed amount after analysis
        * allowed_terms (number): allowed terms after analysis

    """

    loan_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    cpf = UnicodeAttribute()
    birthdate = UnicodeAttribute()
    amount = NumberAttribute()
    terms = NumberAttribute()
    income = NumberAttribute()

    status = UnicodeAttribute(default=LoanAnalysisStatus.PROCESSING.value)
    result = UnicodeAttribute(null=True)
    refused_policy = UnicodeAttribute(null=True)
    allowed_amount = NumberAttribute(null=True)
    allowed_terms = NumberAttribute(null=True)

    class Meta:
        """Schema Meta class."""

        table_name = os.getenv("DYNAMODB_TABLE")
