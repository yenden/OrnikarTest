import argparse
import os
from typing import List, Dict

from dotenv import load_dotenv
from google.cloud import bigquery
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))

from case_study.utils import read_departments_boundaries, construct_department_boundaries_query, valid_date_range

load_dotenv()

# global variables
BOUNDARIES_FILE_PATH = pathlib.Path(__file__).parent.parent / "data/france_department_boundaries.csv"


def get_nb_lessons_by_department(
        partnership_types: List[str],
        start_date: str,
        end_date: str) -> Dict[str, int]:
    """
    Get the number of lessons by departments given a list of partnership types and a data range to include in data.
    
    Args:
    partnership_types (List[str]): the partnership types
    start_date (str): start date to include in data
    end_date (str): end date to include in data

    Returns:
        Dict[str, int]: a dictionary that associate each department to its number of lesson
    """
    # validate inputs
    valid_date_range(start_date, end_date)

    # get the id of the dataset
    dataset_id = os.environ.get("BIGQUERY_DATASET_ID", "")
    # initiate google big query
    client = bigquery.Client()

    # get the department boundaries data
    departments_boundaries = read_departments_boundaries(str(BOUNDARIES_FILE_PATH))
    departments_boundaries_load_query = construct_department_boundaries_query(departments_boundaries)

    # query all the meeting points meeting the criteria
    query = f"""
        WITH dept_lat_long_boundaries AS (
        {departments_boundaries_load_query}
        )
        SELECT
            dept,
            COUNT(DISTINCT l.lesson_id) AS lessons_count
        FROM
                `{dataset_id}.meeting_points` AS mp
            JOIN
                `{dataset_id}.lessons` AS l
            ON
                l.meeting_point_id = mp.meeting_point_id
            JOIN
                `{dataset_id}.bookings` AS b
            ON
                l.lesson_id = b.lesson_id
            JOIN
                `{dataset_id}.instructors` AS i
            ON
                l.instructor_id = i.instructor_id
            JOIN
                dept_lat_long_boundaries AS d
                ON mp.mp_latitude BETWEEN d.south_latitude AND d.north_latitude
                    AND mp.mp_longitude BETWEEN d.west_longitude AND d.east_longitude
            WHERE
                l.lesson_deleted_at IS NULL
                AND b.booking_deleted_at IS NULL
                AND l.lesson_start_at >= TIMESTAMP("{start_date}")
                AND l.lesson_start_at <= TIMESTAMP("{end_date}")
                AND i.partnership_type IN ({', '.join(['"' + pt + '"' for pt in partnership_types])})
            GROUP BY
                dept
    """

    # execute the request
    query_job = client.query(query)
    results = query_job.result()
    # construct the dictionary result
    lessons_by_dept = {}
    for row in results:
        lessons_by_dept.update({row["dept"]: row["lessons_count"]})
    return lessons_by_dept


def parse_cli_args():
    """
    Parse command line argument.
    """
    parser = argparse.ArgumentParser(
        description='Script to get the number of lessons by department given a list of partnership_types')
    parser.add_argument('--partnership-types', type=str, nargs='+',
                        help='partnership_types separated by spaces', required=True)
    parser.add_argument('--start-date',
                        type=str,
                        required=True,
                        help='Start date included in results (format : YYYY-MM-DD)')
    parser.add_argument('--end-date',
                        type=str,
                        required=True,
                        help='End date included in results (format : YYYY-MM-DD)')
    return parser.parse_args()


def main():
    """
    Main function to launch the query to get the number of lessons by department given provided cli arguments.
    """
    args = parse_cli_args()
    results = get_nb_lessons_by_department(partnership_types=args.partnership_types,
                                           start_date=args.start_date,
                                           end_date=args.end_date)
    print("Repartition of lessons by departments")
    print(results)


if __name__ == "__main__":
    main()
