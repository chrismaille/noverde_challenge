"""Loan Model Module."""
import os

from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model


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

    class Meta:
        """Schema Meta class."""

        table_name = os.getenv("DYNAMODB_TABLE")
