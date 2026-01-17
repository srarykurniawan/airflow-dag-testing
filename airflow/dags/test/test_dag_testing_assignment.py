from airflow.models import DagBag

def test_dag_integrity():
    dagbag = DagBag(
        dag_folder="/opt/airflow/dags",
        include_examples=False
    )

    # Pastikan tidak ada error saat load DAG
    assert not dagbag.import_errors

    # Pastikan DAG ada
    dag = dagbag.get_dag("data_validation_dag")
    assert dag is not None

    # Pastikan minimal 3 task
    assert len(dag.tasks) >= 3
