import datetime
from typing import Tuple

import pandas as pd


def read_departments_boundaries(department_location_file: str) -> pd.DataFrame:
    """
    Read departments boundaries that associate each department with its extreme locations (Longitude et Latitude)

    Args:
        department_location_file (str): the file path

    Returns:
        pd.Dataframe: a dataframe containing the department
    """
    departments_boundaries = pd.read_csv(department_location_file)
    departments_boundaries.rename(columns={
        "Latitude la plus au nord": "north_latitude",
        "Latitude la plus au sud": "south_latitude",
        "Longitude la plus à l’est": "east_longitude",
        "Longitude la plus à l’ouest": "west_longitude",
        "Departement": "department"
    }, inplace=True)

    return departments_boundaries


def construct_department_boundaries_query(departments_boundaries: pd.DataFrame) -> str:
    """
    Construct a query that will store department boundaries data.

    Args:
        departments_boundaries (pd.DataFrame): the dataframe containing the department boundaries

    Returns:
        str: a Bigquery Standard SQL request to store department boundaries
    """
    upload_lines = "\tSELECT '" + departments_boundaries["department"].astype(str) + "' AS dept, " \
                   + departments_boundaries["north_latitude"].astype(str) + " AS north_latitude, " \
                   + departments_boundaries["east_longitude"].astype(str) + " AS east_longitude, " \
                   + departments_boundaries["south_latitude"].astype(str) + " AS south_latitude, " \
                   + departments_boundaries["west_longitude"].astype(str) + " AS west_longitude"
    return " UNION ALL\n".join(upload_lines.values.tolist())


def valid_date_range(start_str: str, end_str: str) -> None:
    """
    Validate that dates have ISO format and start <= end.

    Args:
        start_str (str): the start date of the date range
        end_str (str): the end date of the date range

    Raises:
        - TypeError if one of start and end date are not in ISO format
        - ValueError if start date > end date
    """
    try:
        start_date = datetime.date.fromisoformat(start_str)
        end_date = datetime.date.fromisoformat(end_str)
    except ValueError:
        raise TypeError("The dates must be in ISO format (YYYY-MM-DD)")
    if start_date > end_date:
        raise ValueError("The start date must anterior to the end date.")