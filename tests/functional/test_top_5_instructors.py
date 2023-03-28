from datetime import datetime, timezone

import pandas as pd
from pandas._testing import assert_frame_equal

from case_study.top_5_instructors import get_top_5_instructors_and_the_date_of_their_50th_lesson


def test_get_top_5_instructors_and_the_date_of_their_50th_lesson():
    # When
    results = get_top_5_instructors_and_the_date_of_their_50th_lesson()
    # Then
    expected = pd.DataFrame({
        "instructor_id": [280, 128, 22, 250, 292],
        "lesson_50th_date": [datetime(2019, 12, 29, 21, 10, tzinfo=timezone.utc),
                             datetime(2020, 1, 5, 12, 40, tzinfo=timezone.utc),
                             datetime(2020, 1, 4, 22, 2, tzinfo=timezone.utc),
                             datetime(2019, 12, 28, 16, 40, tzinfo=timezone.utc),
                             datetime(2020, 1, 2, 18, 15, tzinfo=timezone.utc)
                             ]

    })
    assert_frame_equal(expected.set_index("instructor_id"),
                       results.set_index("instructor_id"),
                       check_index_type=False, check_like=True)
