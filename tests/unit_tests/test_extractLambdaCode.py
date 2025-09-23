import pytest
from cfn_inline_lambda_linter.linter import extractLambdaCode

def test_extract_lambda_code_valid():
    resources = {
        "LambdaFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.8",
                "Code": {"ZipFile": "print('Hello, Lambda!')\n"}
            }
        }
    }
    dict_to_check = {"LambdaFunction": {"status": "CodeNotFormatted"}}
    result = extractLambdaCode(resources, {}, dict_to_check, args=None)
    assert result["LambdaFunction"]["status"] == "FoundNoErrors"

def test_extract_lambda_code_invalid():
    resources = {
        "LambdaFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.8",
                "Code": {"ZipFile": "print('hello')\nimport sys\nif True\n    print('missing colon')"}  # Clear syntax error
            }
        }
    }
    dict_to_check = {"LambdaFunction": {"status": "CodeNotFormatted"}}
    result = extractLambdaCode(resources, {}, dict_to_check, args=None)
    assert result["LambdaFunction"]["status"] == "FoundErrors"
    assert "E999" in result["LambdaFunction"]["errors"]

def test_extract_lambda_code_missing_zipfile():
    resources = {
        "LambdaFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.8",
                "Code": {}
            }
        }
    }
    dict_to_check = {"LambdaFunction": {"status": "CodeNotFormatted"}}
    result = extractLambdaCode(resources, {}, dict_to_check, args=None)
    # Should skip and leave status unchanged (or set to a specific value if your logic does)
    assert result["LambdaFunction"]["status"] == "SkippingLambda"

def test_extract_lambda_code_ignore_f821():
    """Test that F821 errors are ignored when Lambda code uses CloudFormation substitutions."""
    resources = {
        "LambdaFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.8",
                "Code": {
                    "ZipFile": "import boto3\nimport json\n\n# This would normally trigger F821 - undefined name\nmy_resource = ${MyResource}\nbucket_name = ${BucketName}\n\ndef handler(event, context):\n    return {'statusCode': 200}"
                }
            }
        }
    }
    dict_to_check = {"LambdaFunction": {"status": "CodeNotFormatted"}}
    result = extractLambdaCode(resources, {}, dict_to_check, args=None)
    
    # The linter should ignore F821 errors and not report them as failures
    errors = result["LambdaFunction"].get("errors", "")
    assert "F821" not in errors, "F821 should be ignored for CloudFormation substitutions"
    
    # Since we're ignoring F821, the status should be FoundNoErrors (other errors might still exist)
    # But F821 specifically should not be present
    if result["LambdaFunction"]["status"] == "FoundErrors":
        # If there are errors, make sure F821 is not one of them
        assert "F821" not in errors

def test_extract_lambda_code_ignore_f821_with_custom_args():
    """Test that F821 is still ignored when custom flake8 args are provided."""
    resources = {
        "LambdaFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.8",
                "Code": {
                    "ZipFile": "import boto3\n\n# Variables from CloudFormation substitution\nmy_var = ${MyVariable}\n\ndef handler(event, context):\n    return my_var"
                }
            }
        }
    }
    dict_to_check = {"LambdaFunction": {"status": "CodeNotFormatted"}}
    
    # Test with custom args that don't mention F821
    result = extractLambdaCode(resources, {}, dict_to_check, args="--max-line-length=120")
    
    errors = result["LambdaFunction"].get("errors", "")
    assert "F821" not in errors, "F821 should be ignored even with custom args"

def test_extract_lambda_code_ignore_f821_with_parameter_ref():
    """Test that F821 is ignored when Runtime is referenced via parameter."""
    resources = {
        "LambdaFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "!Ref PythonRuntime",
                "Code": {
                    "ZipFile": "import boto3\n\n# CloudFormation variables\nbucket = ${BucketName}\n\ndef handler(event, context):\n    return bucket"
                }
            }
        }
    }
    parameters = {
        "PythonRuntime": {
            "Default": "python3.8"
        }
    }
    dict_to_check = {"LambdaFunction": {"status": "CodeNotFormatted"}}
    
    result = extractLambdaCode(resources, parameters, dict_to_check, args=None)
    
    errors = result["LambdaFunction"].get("errors", "")
    assert "F821" not in errors, "F821 should be ignored for parameter referenced runtime"
