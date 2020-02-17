from copy import deepcopy

import arrow
import pytest

from noverde_challenge.handlers.analysis import (
    run_age_policy,
    run_commitment_policy,
    run_score_policy,
)
from noverde_challenge.models.loan import LoanAnalysisResult, LoanAnalysisStatus
from noverde_challenge.policies.stakeholders.noverde import NoverdePolicy
from noverde_challenge.utils.handler_task import LoanModel


@pytest.mark.parametrize(
    "age, expected_status, expected_result",
    [
        (-15, LoanAnalysisStatus.COMPLETED.value, LoanAnalysisResult.REFUSED.value),
        (-30, LoanAnalysisStatus.PROCESSING.value, None),
    ],
    ids=["Age: 15 years", "Age: 30 years"],
)
def test_run_age_policy(loan_model, mocker, age, expected_result, expected_status):
    test_loan = deepcopy(loan_model)
    test_loan.birthdate = arrow.utcnow().shift(years=age).format("YYYY-MM-DD")
    mocker.patch.object(LoanModel, "get", return_value=test_loan)
    mocker.patch.object(LoanModel, "save")
    event = {"loan_id": loan_model.loan_id}
    ret = run_age_policy(event, {})
    assert ret == {
        "loan_id": "873649aa-0851-41fe-9a42-6ca6d29ac3d2",
        "status": expected_status,
        "result": expected_result,
    }


@pytest.mark.parametrize(
    "score, expected_status, expected_result",
    [
        (200, LoanAnalysisStatus.COMPLETED.value, LoanAnalysisResult.REFUSED.value),
        (800, LoanAnalysisStatus.PROCESSING.value, None),
    ],
    ids=["Score: 200", "Score 800"],
)
def test_run_score_policy(
    loan_model, mocker, score, expected_result, expected_status, requests_mock
):
    response = {"score": score}
    url = f"{NoverdePolicy.request_base_url}score"
    requests_mock.post(url, json=response)

    mocker.patch.object(LoanModel, "get", return_value=loan_model)
    mocker.patch.object(LoanModel, "save")

    event = {"loan_id": loan_model.loan_id}
    ret = run_score_policy(event, {})
    assert ret == {
        "loan_id": "873649aa-0851-41fe-9a42-6ca6d29ac3d2",
        "status": expected_status,
        "result": expected_result,
    }


@pytest.mark.parametrize(
    "commitment, expected_status, expected_result",
    [(0.95, LoanAnalysisStatus.COMPLETED.value, LoanAnalysisResult.REFUSED.value)],
    ids=["Commitment: 95%"],
)
def test_run_commitment_policy(
    loan_model, mocker, commitment, expected_result, expected_status, requests_mock
):
    response = {"commitment": commitment}
    url = f"{NoverdePolicy.request_base_url}commitment"
    requests_mock.post(url, json=response)

    mocker.patch.object(LoanModel, "get", return_value=loan_model)
    mocker.patch.object(LoanModel, "save")

    event = {"loan_id": loan_model.loan_id}
    ret = run_commitment_policy(event, {})
    assert ret == {
        "loan_id": "873649aa-0851-41fe-9a42-6ca6d29ac3d2",
        "status": expected_status,
        "result": expected_result,
    }
