"""
!!!!!!!CAUTION!!!!!!!
I couldn't get my tests to work with this Bigquery emulator.
But I leave them there to give you an idea of how I would have proceeded.
"""
import os
from datetime import datetime, timedelta

import pandas as pd
import pytest
from google.cloud import bigquery
from testcontainers.core.container import DockerContainer


@pytest.fixture(scope="session", autouse=True)
def bigquery_emulator_container():
    with DockerContainer("ghcr.io/goccy/bigquery-emulator:latest").with_command(
            "--project=test_proj --dataset=test_dataset") as container:
        yield container


@pytest.fixture(scope="session", autouse=True)
def upload_data_to_bq(bigquery_emulator_container):
    os.environ["BIGQUERY_EMULATOR_HOST"] = f"http://0.0.0.0:9050"
    os.environ["BIGQUERY_DATASET_ID"] = "test_proj.test_dataset"
    # Create some example data
    lessons_df = pd.DataFrame({
        'lesson_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'instructor_id': [1, 1, 1, 2, 2, 3, 3, 4, 4, 5],
        'lesson_created_at': [
            datetime(2020, 7, 1),
            datetime(2020, 7, 2),
            datetime(2020, 7, 3),
            datetime(2020, 7, 1),
            datetime(2020, 7, 2),
            datetime(2020, 7, 1),
            datetime(2020, 7, 3),
            datetime(2020, 7, 1),
            datetime(2020, 7, 2),
            datetime(2020, 7, 1)
        ],
        'lesson_deleted_at': [
            None,
            datetime(2020, 7, 2) + timedelta(hours=1),
            datetime(2020, 7, 3) + timedelta(hours=1),
            None,
            datetime(2020, 7, 2) + timedelta(hours=1),
            None,
            datetime(2020, 7, 3) + timedelta(hours=1),
            None,
            None,
            None
        ]
    })

    instructors_df = pd.DataFrame({
        'instructor_id': [1, 2, 3, 4, 5],
        'partnership_type': ['FT', 'MT', 'MT', 'FT', 'FT']
    })

    bookings_df = pd.DataFrame({
        'booking_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'learner_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'lesson_id': [1, 2, 3, 1, 2, 1, 3, 2, 3, 1],
        'booking_created_at': [
            datetime(2020, 7, 1) + timedelta(hours=1),
            datetime(2020, 7, 2) + timedelta(hours=1),
            datetime(2020, 7, 3) + timedelta(hours=1),
            datetime(2020, 7, 1) + timedelta(hours=1),
            datetime(2020, 7, 2) + timedelta(hours=1),
            datetime(2020, 7, 1) + timedelta(hours=1),
            datetime(2020, 7, 3) + timedelta(hours=1),
            datetime(2020, 7, 1) + timedelta(hours=1),
            datetime(2020, 7, 2) + timedelta(hours=1),
            datetime(2020, 7, 1) + timedelta(hours=1)
        ],
        'booking_deleted_at': [None] * 10
    })

    meeting_points_df = pd.DataFrame({
        'meeting_point_id': [1, 2, 3, 4, 5],
        'mp_latitude': [48.8566, 48.8534, 48.8606, 48.8647, 48.8508],
        'mp_longitude': [2.3522, 2.3488, 2.3522, 2.3490, 2.2986]
    })
    # create dataset
    client = bigquery.Client()
    write_df_to_bq(client, lessons_df, "lessons")
    write_df_to_bq(client, instructors_df, "instructors")
    write_df_to_bq(client, bookings_df, "bookings")
    write_df_to_bq(client, meeting_points_df, "meeting_points")


def write_df_to_bq(client, df, table_name):
    dataset_id = "test_proj.test_dataset"
    table_id = f'{dataset_id}.{table_name}'
    job_config = bigquery.LoadJobConfig(
        write_disposition='WRITE_TRUNCATE',
        autodetect=True
    )
    client.load_table_from_dataframe(df, table_id, job_config=job_config, timeout=60).result()
