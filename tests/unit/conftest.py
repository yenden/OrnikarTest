from unittest import mock

import pytest


@pytest.fixture
def mock_bq_client():
    with mock.patch("google.cloud.bigquery.Client") as mock_client:
        yield mock_client


@pytest.fixture
def mock_csv():
    with mock.patch("case_study.utils.pd.read_csv") as mock_read_csv:
        yield mock_read_csv

