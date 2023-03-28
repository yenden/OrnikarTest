import pandas as pd
from pandas._testing import assert_frame_equal

from case_study.top_5_instructors import get_top_5_instructors_and_the_date_of_their_50th_lesson


def test_get_top_5_instructors_and_the_date_of_their_50th_lesson(mock_bq_client):
    # Given
    expected_data = pd.DataFrame({
        "instructor_id": [1, 2, 3, 4, 5],
        "lesson_50th_date": ["2020-01-01"] * 5
    })
    mock_bq_client.return_value.query().to_dataframe.return_value = expected_data

    # When
    result = get_top_5_instructors_and_the_date_of_their_50th_lesson()

    # Then
    assert_frame_equal(expected_data, result)
