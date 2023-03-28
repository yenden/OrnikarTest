import pytest

from case_study.lessons_by_department import get_nb_lessons_by_department


def test_get_nb_lessons_by_department(mock_bq_client, mock_csv):
    mock_bq_client.return_value.query().result.return_value = [
        {'dept': 'dept1', 'lessons_count': 10},
        {'dept': 'dept2', 'lessons_count': 15}
    ]

    result = get_nb_lessons_by_department(partnership_types=["p1", "p2"],
                                          start_date="2020-08-01",
                                          end_date="2020-09-01")
    expected = {'dept1': 10, 'dept2': 15}

    assert expected == result


def test_get_nb_lessons_by_department_invalid_inputs():
    with pytest.raises(ValueError):
        get_nb_lessons_by_department(partnership_types=["p1", "p2"],
                                     start_date="2020-08-01",
                                     end_date="2020-07-01")
