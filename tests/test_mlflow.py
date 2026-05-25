import mlflow
import os

def test_mlflow_experiment_creation():
    mlflow.set_experiment("test-experiment")
    client = mlflow.tracking.MlflowClient()
    exp    = client.get_experiment_by_name("test-experiment")
    assert exp is not None
    assert exp.name == "test-experiment"

def test_mlflow_log_metrics():
    mlflow.set_experiment("test-experiment")
    with mlflow.start_run():
        mlflow.log_param("test_param", 42)
        mlflow.log_metric("test_metric", 0.95)
        run_id = mlflow.active_run().info.run_id

    client = mlflow.tracking.MlflowClient()
    run    = client.get_run(run_id)
    assert run.data.metrics["test_metric"] == 0.95
    assert run.data.params["test_param"] == "42"

def test_mlruns_folder_created():
    assert os.path.exists("mlruns")

if __name__ == "__main__":
    test_mlflow_experiment_creation()
    test_mlflow_log_metrics()
    test_mlruns_folder_created()
    print("All MLflow tests passed.")