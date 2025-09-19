from unittest.mock import patch

@patch("cfn_inline_lambda_linter.linter.subprocess.Popen")
def test_flake8_linting(mock_popen):
    mock_process = mock_popen.return_value
    mock_process.communicate.return_value = (b"", b"")
    mock_process.returncode = 0

    resources = {
        "LambdaFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.8",
                "Code": {"ZipFile": "print('Hello, Lambda!')"}
            }
        }
    }
    dict_to_check = {"LambdaFunction": {"status": "CodeNotFormatted"}}
    from cfn_inline_lambda_linter.linter import extractLambdaCode
    result = extractLambdaCode(resources, {}, dict_to_check, args=None)
    assert result["LambdaFunction"]["status"] == "FoundNoErrors"
