import os
import json
from src.utils.file_utils import load_json, save_json, ensure_dir

def test_save_and_load_json():
    path = "data/processed/test_temp.json"
    data = {"key": "value", "number": 42}
    save_json(data, path)
    loaded = load_json(path)
    assert loaded["key"] == "value"
    assert loaded["number"] == 42
    os.remove(path)

def test_ensure_dir():
    ensure_dir("data/processed/test_dir")
    assert os.path.exists("data/processed/test_dir")
    os.rmdir("data/processed/test_dir")

if __name__ == "__main__":
    test_save_and_load_json()
    test_ensure_dir()
    print("All tests passed.")