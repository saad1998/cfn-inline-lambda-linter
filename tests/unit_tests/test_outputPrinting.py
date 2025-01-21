from cfn_inline_lambda_linter.linter import outputPrinting

def test_output_printing_no_errors(capsys):
    error_dict = {
        "LambdaFunction": {"status": "FoundNoErrors"}
    }
    result = outputPrinting(error_dict)
    captured = capsys.readouterr()
    assert result is True
    assert "✅" in captured.out

def test_output_printing_with_errors(capsys):
    error_dict = {
        "LambdaFunction": {"status": "FoundErrors", "errors": "E999 SyntaxError: invalid syntax"}
    }
    result = outputPrinting(error_dict)
    captured = capsys.readouterr()
    assert result is False
    assert "❌" in captured.out
