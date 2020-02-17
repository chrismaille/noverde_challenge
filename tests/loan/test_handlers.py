import json
import uuid
from copy import deepcopy

import pytest
from pynamodb.exceptions import DoesNotExist

from noverde_challenge.handlers.loan import get, post
from noverde_challenge.utils.status_code import StatusCode

good_dog = {
    "terms": 12,
    "name": "Seu Madruga",
    "cpf": "077.244.260-66",
    "amount": 1000.0,
    "birthdate": "1923-09-02",
    "income": 2000.0,
}


def test_get(loan_model, mocker):
    from noverde_challenge.handlers.loan import LoanModel

    mocker.patch.object(LoanModel, "get", return_value=loan_model)
    response = get(
        {"pathParameters": {"loan_id": "873649aa-0851-41fe-9a42-6ca6d29ac3d2"}}, {}
    )
    assert response["statusCode"] == StatusCode.OK.value
    assert json.loads(response["body"]) == {
        "amount": None,
        "id": "873649aa-0851-41fe-9a42-6ca6d29ac3d2",
        "refused_policy": None,
        "result": None,
        "status": "processing",
        "terms": None,
    }


def test_get_not_found(mocker):
    from noverde_challenge.handlers.loan import LoanModel

    mocker.patch.object(LoanModel, "get", side_effect=DoesNotExist)
    response = get(
        {"pathParameters": {"loan_id": "873649aa-0851-41fe-9a42-6ca6d29ac3d2"}}, {}
    )
    assert response["statusCode"] == StatusCode.NOT_FOUND.value
    assert json.loads(response["body"]) == {
        "errors": ["LoanId 873649aa-0851-41fe-9a42-6ca6d29ac3d2 does not found."]
    }


@pytest.mark.parametrize(
    "field,value,error_message",
    [
        ("terms", 5, "Terms must be one of"),
        ("cpf", "1234", "cpf: Invalid CPF number."),
        ("amount", 15000, "Amount must be between"),
        ("birthdate", None, "birthdate: Field may not be null"),
    ],
    ids=["Bad Terms", "Bad CPF", "Bad Amount", "Missing Birthday"],
)
def test_invalid_post(field, value, error_message):
    bad_dog = deepcopy(good_dog)
    bad_dog[field] = value

    event = {"body": json.dumps(bad_dog)}
    response = post(event, {})
    assert response["statusCode"] == StatusCode.BAD_REQUEST.value
    assert error_message in response["body"]


def test_post(mocker):
    from noverde_challenge.schemas.loan import LoanModel

    mocker.patch.object(LoanModel, "save")
    mocker.patch.object(LoanModel, "exists", return_value=False)
    mocker.patch.object(LoanModel, "create_table")

    event = {"body": json.dumps(good_dog)}
    response = post(event, {})
    assert response["statusCode"] == StatusCode.CREATED.value
    response = json.loads(response["body"])
    uuid_value = response["id"]
    assert uuid.UUID(uuid_value)


def test_internal_server_error():
    event = {"body": "ERROR"}
    response = post(event, {})
    assert response["statusCode"] == 500
    assert (
        response["body"] == '{"error": ["Expecting value: line 1 column 1 (char 0)"]}'
    )
