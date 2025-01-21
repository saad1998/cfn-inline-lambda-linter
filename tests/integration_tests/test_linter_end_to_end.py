from cfn_inline_lambda_linter.linter import linter

def test_linter_valid_template(tmp_path, monkeypatch):
    file_path = tmp_path / "valid_template.yaml"
    file_path.write_text("""
    Resources:
      LambdaFunction:
        Type: "AWS::Lambda::Function"
        Properties:
          Runtime: "python3.8"
          Code:
            ZipFile: "print('Hello, Lambda!')"
    """)
    monkeypatch.setattr("sys.exit", lambda x: x)  # Prevent pytest from exiting
    linter(str(file_path))

def test_linter_template_with_errors(tmp_path, monkeypatch):
    file_path = tmp_path / "error_template.yaml"
    file_path.write_text("""
    Resources:
      LambdaFunction:
        Type: "AWS::Lambda::Function"
        Properties:
          Runtime: "python3.8"
          Code:
            ZipFile: "print(Hello, Lambda!)"
    """)
    monkeypatch.setattr("sys.exit", lambda x: x)  # Prevent pytest from exiting
    linter(str(file_path))
