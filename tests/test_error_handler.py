import pytest
from fastapi import HTTPException
from src.utils.error_handler import handle_validation_error, safe_divide

def test_handle_validation_error_raises():
    with pytest.raises(HTTPException) as exc:
        handle_validation_error(["age is required"])
    assert exc.value.status_code == 422

def test_handle_validation_error_passes():
    handle_validation_error([])

def test_safe_divide():
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(10, 0) == 0.0
    assert safe_divide(10, 0, default=1.0) == 1.0

if __name__ == "__main__":
    test_handle_validation_error_raises()
    test_handle_validation_error_passes()
    test_safe_divide()
    print("All tests passed.")