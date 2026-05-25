from dagster import job, op
import os

@op
def ingest(_):
    os.system("python pipeline/ingest.py")

@op
def validate(_, ingest_result):
    os.system("python pipeline/validate.py")

@op
def transform(_, validate_result):
    os.system("cd dbt_pipeline && dbt run --profiles-dir .")

@op
def test_data(_, transform_result):
    os.system("cd dbt_pipeline && dbt test --profiles-dir .")

@job
def ventes_pipeline():
    test_data(transform(validate(ingest())))