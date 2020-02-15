from noverde_challenge.models.loan import LoanModel


def test_model_attributes():
    attributes = ["loan_id", "name", "cpf", "birthdate", "amount", "terms", "income"]
    for attribute in attributes:
        assert attribute in dir(LoanModel)
