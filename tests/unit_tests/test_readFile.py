import pytest
from cfn_inline_lambda_linter.linter import readFile
import yaml


def test_read_file_valid(tmp_path):
    file_path = tmp_path / "template.yaml"
    file_path.write_text("""
    Resources:
      LambdaFunction:
        Type: "AWS::Lambda::Function"
        Properties:
          Runtime: "python3.12"
          Code:
            ZipFile: "print('Hello, world!')"
    """)
    result = readFile(str(file_path))
    assert "Resources" in result


def test_read_file_not_found():
    with pytest.raises(FileNotFoundError):
        readFile("non_existent.yaml")
