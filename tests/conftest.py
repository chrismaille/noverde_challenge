"""Pytest Configuration file."""
from pytest import fixture

from noverde_challenge.models.loan import LoanModel


@fixture
def loan_model():
    """Loan Model Fixture."""
    data = {
        "loan_id": "873649aa-0851-41fe-9a42-6ca6d29ac3d2",
        "amount": 500.00,
        "cpf": "077.244.260-67",
        "birthdate": "1923-09-02",
        "terms": 12,
        "name": "Seu Madruga",
        "income": 3000.00,
    }
    return LoanModel(**data)
