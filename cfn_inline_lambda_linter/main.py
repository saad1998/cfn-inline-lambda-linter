import typer
import sys
import io
from typing import List
from .linter import linter

LANGUAGES = ["python"]
app = typer.Typer()

@app.callback()
def callback():
    """
    CILL: CFN Inline Lambda Linter
    """

@app.command()
def lint(
    files: List[str] = typer.Argument(
        None,
        help="List of files passed by pre-commit or manually."
    ),
    args_to_pass_to_lint: str = typer.Option(
        None,
        "--args",
        "-a",
        help="Additional arguments to pass to the linter as a single string separated by space like: --max-line-length=88 --ignore=E203,W503",
        show_default=True,
    )
):
    """
    Lets start linting
    """
    overall_success = True  # Track overall success status
    output_buffer = io.StringIO()  # Buffer for capturing output

    # Temporarily redirect stdout and stderr to the buffer
    sys.stdout = output_buffer
    sys.stderr = output_buffer
    
    if args_to_pass_to_lint is not None:
        validate_args(args_to_pass_to_lint)

    try:
        for file in files:
            try:
                if args_to_pass_to_lint is None:
                    linter(file)
                else:
                    linter(file,args_to_pass_to_lint)
            except SystemExit as e:
                if e.code != 0:
                    overall_success = False
            except Exception as e:
                overall_success = False
                print(f"Unexpected error while linting {file}: {e}", file=sys.stderr)

    finally:
        # Restore original stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    if overall_success:
        # No errors; suppress output
        print("✅ All files passed linting!")
    else:
        # Errors found; print the buffered output
        print("❌ Some files failed linting. See details below:\n")
        print(output_buffer.getvalue())

    # Exit with the appropriate status code
    sys.exit(0 if overall_success else 1)


def validate_args(args: str) -> None:
    """
    Validates the `args_to_pass_to_lint` option to ensure correct formatting.
    """
    if args:
        # Ensure no leading or trailing spaces
        if args != args.strip():
            raise typer.BadParameter("Arguments must not have leading or trailing spaces.")
        # Ensure no double spaces within the string
        if "  " in args:
            raise typer.BadParameter("Arguments must be separated by a single space only.")
