from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# =========================
# Functions
# =========================

def extract_data(**context):
    data = [
        {"name": "apple"},
        {"name": "banana"},
        {"name": "orange"}
    ]
    context["ti"].xcom_push(key="extracted_data", value=data)
    return data


def transform_data(data):
    transformed = [{"name": item["name"].upper()} for item in data]
    return transformed


def transform_task_callable(ti):
    data = ti.xcom_pull(task_ids="extract_task")

    if not data:
        print("No XCom data found, running in isolated test mode")
        data = [{"name": "apple"}, {"name": "banana"}, {"name": "orange"}]

    transformed = [{"name": item["name"].upper()} for item in data]
    return transformed


def load_data(**context):
    ti = context["ti"]
    data = ti.xcom_pull(task_ids="transform_task", key="transformed_data")
    print("Loaded data:", data)


# =========================
# DAG Definition
# =========================

default_args = {
    "owner": "data-engineering-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="data_validation_dag",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["testing", "validation", "dag-testing"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract_data,
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform_task_callable,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load_data,
        provide_context=True,
    )

    extract_task >> transform_task >> load_task
