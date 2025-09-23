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
    """)
    monkeypatch.setattr("sys.exit", lambda x: x)  # Prevent pytest from exiting
    linter(str(file_path))

def test_linter_lambda_without_inline_code(tmp_path, monkeypatch):
    """Test scenario when Lambda Function does not have inline code (should be skipped)"""
    file_path = tmp_path / "no_inline_code_template.yaml"
    file_path.write_text("""
    Resources:
      LambdaFunction:
        Type: "AWS::Lambda::Function"
        Properties:
          Runtime: "python3.8"
          Code:
            S3Bucket: "my-bucket"
            S3Key: "lambda.zip"
    """)
    monkeypatch.setattr("sys.exit", lambda x: x)  # Prevent pytest from exiting
    linter(str(file_path))

def test_linter_lambda_with_parameter_runtime(tmp_path, monkeypatch):
    """Test scenario when Lambda Function has a parameter for Runtime"""
    file_path = tmp_path / "parameter_runtime_template.yaml"
    file_path.write_text("""
    Parameters:
      LambdaRuntime:
        Type: String
        Default: "python3.9"
        
    Resources:
      LambdaFunction:
        Type: "AWS::Lambda::Function"
        Properties:
          Runtime: !Ref LambdaRuntime
          Code:
            ZipFile: "print('Hello from parameterized runtime!')"
    """)
    monkeypatch.setattr("sys.exit", lambda x: x)  # Prevent pytest from exiting
    linter(str(file_path))

def test_linter_simple_yaml_not_cloudformation(tmp_path, monkeypatch):
    """Test scenario when file is a simple YAML file that is not a CloudFormation template (should be skipped)"""
    file_path = tmp_path / "simple_yaml.yaml"
    file_path.write_text("""
    name: "My Application"
    version: "1.0.0"
    dependencies:
      - python: "3.8"
      - flask: "2.0.1"
    config:
      debug: true
      port: 8080
    """)
    
    # Use SystemExit exception to properly handle sys.exit()
    import pytest
    with pytest.raises(SystemExit) as exc_info:
        linter(str(file_path))
    
    # Should exit with code 0 (success) since it's skipping the file
    assert exc_info.value.code == 0

def test_linter_lambda_with_sub_function_ignores_f821(tmp_path, monkeypatch):
    """Test that F821 errors are ignored when Lambda code uses !Sub with CloudFormation parameters/resources"""
    file_path = tmp_path / "lambda_with_sub_template.yaml"
    file_path.write_text("""
    Parameters:
      BucketName:
        Type: String
        Default: "my-test-bucket"
        
    Resources:
      MyS3Bucket:
        Type: "AWS::S3::Bucket"
        Properties:
          BucketName: !Ref BucketName
          
      LambdaFunction:
        Type: "AWS::Lambda::Function"
        Properties:
          Runtime: "python3.8"
          Code:
            ZipFile: !Sub |
              import boto3
              bucket_name = "${BucketName}"
              s3_bucket = "${MyS3Bucket}"
              def lambda_handler(event, context):
                  print(f"Bucket name: {bucket_name}")
                  print(f"S3 bucket: {s3_bucket}")
                  return {"statusCode": 200}
    """)
    monkeypatch.setattr("sys.exit", lambda x: x)  # Prevent pytest from exiting
    linter(str(file_path))
