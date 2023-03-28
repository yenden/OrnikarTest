import pandas as pd
import pytest

from case_study.top_5_instructors import get_top_5_instructors_and_the_date_of_their_50th_lesson


@pytest.mark.skip("I couldn't get my tests to work with this Bigquery emulator."
                  "But I leave them there to give you an idea of how I would have proceeded.")
def test_get_top_5_instructors_and_the_date_of_their_50th_lesson():
    # When
    results = get_top_5_instructors_and_the_date_of_their_50th_lesson()
    # Then
    expected = pd.DataFrame()  # TODO
    assert expected == results
