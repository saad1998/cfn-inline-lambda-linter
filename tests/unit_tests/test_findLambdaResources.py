from cfn_inline_lambda_linter.linter import findLambdaResources

def test_find_lambda_resources():
    resources = {
        "LambdaFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.12",
                "Code": {"ZipFile": "print('Hello, Lambda!')"}
            }
        },
        "NonLambdaResource": {
            "Type": "AWS::S3::Bucket"
        }
    }
    result = findLambdaResources(resources)
    assert "LambdaFunction" in result
    assert result["LambdaFunction"]["status"] == "CodeNotFormatted"

def test_find_no_lambda_resources():
    resources = {
        "NonLambdaResource": {
            "Type": "AWS::S3::Bucket"
        }
    }
    result = findLambdaResources(resources)
    assert result == {}
