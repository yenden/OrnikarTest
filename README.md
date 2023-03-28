# Case Study Data Engineer

This project contains scripts and tests about the Data Engineer Case Study at Ornikar.

It contains code analysing the top 5 instructors and lessons by department. It also contains responses to questions of
the second part of the case study

The project structure is as follows:

- case_study/: contains the main Python files for the analysis
- data/: contains a CSV file with department boundaries in France
- tests/: contains unit, functional, and integration tests for the code
- requirements.txt: a file with the necessary dependencies for running the code
- requirements-dev.txt: a file with additional dependencies for running tests
- architecture_questions/: a directory containing my responses for the Part 2 case study questions

## Pre-requisites

Make sure you have Python3.X and pip installed. For integration tests you will need docker installed.

## Installation

1. Clone the repository: `git clone https://github.com/yenden/OrnikarTest.git`
2. Change into the project directory: cd OrnikarTest
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate.bat`
    - On macOS or `Linux: source venv/bin/activate`
5. Install the required packages: `pip install -r requirements.txt`
6. If you also want to run the tests, you will need to install the additional dependencies listed in
   requirements-dev.txt. Run: `pip install -r requirements-dev.txt`

## Testing

To run the tests, you can use the `pytest` command from the root directory of the project. For example:

```bash
python -m pytest tests/
```

## Usage

### Pre-Requisites
All the scripts reads the BigQuery dataset ID from the BIGQUERY_DATASET_ID environment variable, so make sure to set it before running the script.

### The top 5 instructors
This script allows you to get for each of the top 5 instructors who gave the most lessons on Q3 2020, the date they gave their 50th lesson.
```bash
python case_study/top_5_instructors.py
```
### The repartition of lessons by department

This script allows you to get the number of lessons by department given a list of partnership types and a date range to
include in the data.

```bash
python case_study/lessons_by_department.py --partnership-types p1 p2 --start-date 2020-07-01 --end-date 2020-08-01
```
Where:
- partnership-types is the list of partnership types separated by spaces
- start-date is the start date included in the results (format: YYYY-MM-DD)
- end-date is the end date included in the results (format: YYYY-MM-DD)
