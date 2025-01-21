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
    result = extractLambdaCode(resources, dict_to_check, {})
    assert result["LambdaFunction"]["status"] == "FoundNoErrors"

def test_extract_lambda_code_invalid():
    resources = {
        "LambdaFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.8",
                "Code": {"ZipFile": "print(Hello, Lambda!)"}  # Syntax error
            }
        }
    }
    dict_to_check = {"LambdaFunction": {"status": "CodeNotFormatted"}}
    result = extractLambdaCode(resources, dict_to_check, {})
    assert result["LambdaFunction"]["status"] == "FoundErrors"
    assert "SyntaxError" in result["LambdaFunction"]["errors"]

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
    with pytest.raises(KeyError):
        extractLambdaCode(resources, dict_to_check, {})
