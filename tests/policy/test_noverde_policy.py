from copy import deepcopy

import arrow
import pytest

from noverde_challenge.policies.stakeholders.noverde import NoverdePolicy


def test_request_score(loan_model, requests_mock):
    response = {"score": 800}
    policy = NoverdePolicy(loan=loan_model)
    url = f"{policy.request_base_url}score"
    requests_mock.post(url, json=response)
    score = policy.request_score()
    assert score == 800


def test_request_commitment(loan_model, requests_mock):
    response = {"commitment": 0.8}
    policy = NoverdePolicy(loan=loan_model)
    url = f"{policy.request_base_url}commitment"
    requests_mock.post(url, json=response)
    commitment = policy.request_commitment()
    assert commitment == 0.8


@pytest.mark.parametrize(
    "value, result",
    [(500.0, False), (2000.0, True), (6000.0, False)],
    ids=["Below minimum", "Good Value", "Above maximum"],
)
def test_amount_policy(loan_model, value, result):
    policy = NoverdePolicy(loan=loan_model)
    assert policy.run_amount_policy(value) == result


@pytest.mark.parametrize(
    "value, result", [(15, False), (30, True)], ids=["Below 18", "Above 18"]
)
def test_age_policy(loan_model, value, result):
    test_loan = deepcopy(loan_model)
    test_loan.birthdate = arrow.utcnow().shift(years=value * -1).format("YYYY-MM-DD")
    policy = NoverdePolicy(loan=test_loan)
    assert policy.run_age_policy() == result


@pytest.mark.parametrize(
    "value, result", [(800, True), (200, False)], ids=["Good Score", "Bad Score"]
)
def test_score_policy(loan_model, value, result, requests_mock):
    response = {"score": value}
    policy = NoverdePolicy(loan=loan_model)
    url = f"{policy.request_base_url}score"
    requests_mock.post(url, json=response)
    assert policy.run_score_policy() == result


@pytest.mark.parametrize(
    "value, result", [(9, True), (3, False)], ids=["Good Terms", "Bad Terms"]
)
def test_terms_policy(loan_model, value, result):
    policy = NoverdePolicy(loan=loan_model)
    assert policy.run_terms_policy(value) == result


@pytest.mark.parametrize(
    "value, result", [(800, False), (200, True)], ids=["Good Score", "Bad Score"]
)
def test_commitment_policy(loan_model, value, result, requests_mock):
    response = {"commitment": 0.8}
    test_model = deepcopy(loan_model)
    test_model.income = 3000.00
    policy = NoverdePolicy(loan=test_model)
    url = f"{policy.request_base_url}commitment"
    requests_mock.post(url, json=response)
    assert policy.run_commitment_policy(pmt=value) == result


def test_calculate_pmt():
    pmt = NoverdePolicy.calculate_pmt(
        present_value=5000, rate_interest=0.15, number_period=12
    )
    assert pmt == 922.40
