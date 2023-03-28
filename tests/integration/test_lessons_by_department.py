import pytest

from case_study.lessons_by_department import get_nb_lessons_by_department


@pytest.mark.skip("I couldn't get my tests to work with this Bigquery emulator."
                  "But I leave them there to give you an idea of how I would have proceeded.")
def test_get_nb_lessons_by_department():
    # When
    results = get_nb_lessons_by_department(partnership_types=["FT"],
                                           start_date="2020-07-01",
                                           end_date="2020-07-03")
    # Then
    expected = {}  # TODO
    assert expected == results
