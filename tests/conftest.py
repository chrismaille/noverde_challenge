"""Pytest Configuration file."""
import numpy as np
import pandas as pd
from pytest import fixture

from noverde_challenge.models.loan import LoanModel


@fixture
def loan_model():
    """Loan Model Fixture."""
    data = {
        "loan_id": "873649aa-0851-41fe-9a42-6ca6d29ac3d2",
        "amount": 3000.00,
        "cpf": "077.244.260-67",
        "birthdate": "1923-09-02",
        "terms": 9,
        "name": "Seu Madruga",
        "income": 1500.00,
        "status": "processing",
        "result": None,
        "refused_policy": None,
        "allowed_amount": None,
        "allowed_terms": None,
    }
    return LoanModel(**data)


@fixture
def test_rate_model():
    """Return a Test Interest Rate Model."""
    df = pd.DataFrame(
        np.array(
            (
                [600, 0.080, 0.085, 0.090],
                [700, 0.065, 0.070, 0.075],
                [800, 0.050, 0.055, 0.060],
                [900, 0.035, 0.040, 0.045],
            )
        ),
        columns=["score", "6", "9", "12"],
    )
    return df
