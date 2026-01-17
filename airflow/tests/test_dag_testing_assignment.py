import pytest
from airflow.models import DagBag
from dags.dag_testing_assignment import transform_data

# =========================
# Pytest Fixture
# =========================

@pytest.fixture
def sample_data():
    return [
        {"name": "apple"},
        {"name": "banana"}
    ]


# =========================
# Unit Test Function
# =========================

def test_transform_data(sample_data):
    result = transform_data(sample_data)
    assert result == [
        {"name": "APPLE"},
        {"name": "BANANA"}
    ]


# =========================
# DAG Integrity Test
# =========================

def test_dag_integrity():
    dagbag = DagBag(dag_folder="airflow/dags", include_examples=False)
    assert not dagbag.import_errors

    dag = dagbag.get_dag("data_validation_dag")
    assert dag is not None
    assert len(dag.tasks) >= 3
