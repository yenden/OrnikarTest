from contextlib import nullcontext as does_not_raise

import pandas as pd
import pytest
from pandas._testing import assert_frame_equal

from case_study.utils import read_departments_boundaries, construct_department_boundaries_query, valid_date_range


def test_read_departments_boundaries(mock_csv):
    # Given
    mock_file = "department_location_file.csv"
    mock_df = pd.DataFrame({
        "Latitude la plus au nord": [50.0, 51.0],
        "Latitude la plus au sud": [49.0, 50.0],
        "Longitude la plus à l’est": [2.0, 3.0],
        "Longitude la plus à l’ouest": [1.0, 2.0],
        "Departement": ["A", "B"]
    })
    mock_csv.return_value = mock_df

    # When
    result = read_departments_boundaries(mock_file)

    # Then
    expected_df = pd.DataFrame({
        "north_latitude": [50.0, 51.0],
        "south_latitude": [49.0, 50.0],
        "east_longitude": [2.0, 3.0],
        "west_longitude": [1.0, 2.0],
        "department": ["A", "B"]
    })
    assert_frame_equal(result, expected_df)


def test_construct_department_boundaries_query():
    # Given
    departments_boundaries = pd.DataFrame({
        "north_latitude": [50.0, 51.0],
        "south_latitude": [49.0, 50.0],
        "east_longitude": [2.0, 3.0],
        "west_longitude": [1.0, 2.0],
        "department": ["A", "B"]
    })

    # When
    result = construct_department_boundaries_query(departments_boundaries)

    # Then
    expected = "\tSELECT 'A' AS dept, 50.0 AS north_latitude, 2.0 AS east_longitude, 49.0 AS south_latitude," \
               " 1.0 AS west_longitude UNION ALL\n" \
               "\tSELECT 'B' AS dept, 51.0 AS north_latitude, 3.0 AS east_longitude, 50.0 AS south_latitude," \
               " 2.0 AS west_longitude"
    assert expected == result


@pytest.mark.parametrize("start_str, end_str", [
    ("2020-09-01", "2020-12-01"),
    ("2022-01-01", "2022-01-01")
])
def test_valid_date_range(start_str, end_str):
    # Given
    # When
    valid_date_range(start_str, end_str)


@pytest.mark.parametrize(
    "start_str, end_str, expectation, message",
    [
        ("2020-09-01", "2020-12-01", does_not_raise(), None),
        ("2022-01-01", "2022-01-01", does_not_raise(), None),
        ("09-2020-01", "2020-12-01", pytest.raises(TypeError), "The dates must be in ISO format"),
        ("2020-01-09", "12-2020-01", pytest.raises(TypeError), "The dates must be in ISO format"),
        ("2020-09-01", "2020-08-01", pytest.raises(ValueError), "The start date must anterior to the end date"),
    ],
)
def test_valid_date_range(start_str, end_str, expectation, message):
    with expectation as e:
        valid_date_range(start_str, end_str)
    assert message is None or message in str(e)
