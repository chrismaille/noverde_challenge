from noverde_challenge.policies.stakeholders.noverde import NoverdePolicy
from noverde_challenge.schemas.loan import LoanModelSchema


def test_policy_class_in_schema(loan_model):
    policy = LoanModelSchema()
    assert policy.policy_class == NoverdePolicy
