import json

from NoverdeChallenge import __version__
from NoverdeChallenge.handler import hello


def test_version():
    assert __version__ == "0.1.0"


def test_hello_event():
    ret = hello({}, {})
    assert ret == {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Go Serverless v1.0! Your function executed successfully!",
                "input": {},
            }
        ),
    }
