import os

import pandas as pd
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()


def get_top_5_instructors_and_the_date_of_their_50th_lesson() -> pd.DataFrame:
    """
    For each of the top 5 instructors who gave the most lessons on Q3 2020,
    this will return the date in which they gave their 50th lesson was carried out

    Returns:
        pd.DataFrame: results in a dataframe
    """
    # create the BQ client library
    client = bigquery.Client()
    dataset_id = os.environ.get("BIGQUERY_DATASET_ID", "")
    query = f"""
    WITH
      instructor_lesson_count AS (
        SELECT
          instructor_id,
          COUNT(DISTINCT lessons.lesson_id) AS lesson_count
        FROM
          `{dataset_id}.bookings` AS bookings
          JOIN `{dataset_id}.lessons` AS lessons ON bookings.lesson_id = lessons.lesson_id
        WHERE
          format_date('%Q(%Y)', date(booking_created_at)) = "3(2020)"
          AND lesson_deleted_at IS NULL
          AND booking_deleted_at IS NULL
        GROUP BY
          instructor_id
        ORDER BY
          lesson_count DESC
        LIMIT
          5
      ),

      instructor_50th_lesson AS (
        SELECT
          instructor_id,
          booking_created_at AS lesson_50th_date
        FROM
          (
            SELECT
              instructor_id,
              booking_created_at,
              ROW_NUMBER() OVER (PARTITION BY instructor_id ORDER BY booking_created_at) AS lesson_num
            FROM
              `{dataset_id}.bookings` AS bookings
              JOIN `{dataset_id}.lessons` AS lessons ON bookings.lesson_id = lessons.lesson_id
            WHERE
              lesson_deleted_at IS NULL
              AND booking_deleted_at IS NULL
          ) t
        WHERE
          t.lesson_num = 50
      )

    SELECT
      instructors.instructor_id,
      lesson_50th_date,
    FROM
      instructor_lesson_count
      JOIN `{dataset_id}.instructors` AS instructors ON instructor_lesson_count.instructor_id = instructors.instructor_id
      JOIN instructor_50th_lesson ON instructor_lesson_count.instructor_id = instructor_50th_lesson.instructor_id
    """
    # query the job
    query_job = client.query(query)
    # get the results
    results_df = query_job.to_dataframe(create_bqstorage_client=False)
    return results_df


if __name__ == '__main__':
    results = get_top_5_instructors_and_the_date_of_their_50th_lesson()
    print(f"Results of top 5 instructors and the date of their 50th lesson")
    print(results)

