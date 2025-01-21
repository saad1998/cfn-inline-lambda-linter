import yaml
import subprocess
import sys
from colorama import Fore, Style
from pathlib import Path


def readFile(fileName):
    """
    Reads a CloudFormation template file and parses its content.

    Args:
        fileName (str): The name of the file to read and parse.

    Returns:
        dict: The parsed CloudFormation template.
    """
    print(Fore.CYAN + f"📂 Reading and parsing the template file: {fileName}..." + Style.RESET_ALL)
    
    try:
        with open(fileName, 'r') as file:
            template = yaml.load(file, Loader=yaml.BaseLoader)
        print(Fore.GREEN + f"✅ Successfully read and parsed the template file: {fileName}" + Style.RESET_ALL)
        return template
    except FileNotFoundError:
        print(Fore.RED + f"❌ Error: File '{fileName}' not found." + Style.RESET_ALL)
        raise
    except yaml.YAMLError as e:
        print(Fore.RED + f"❌ Error parsing YAML in file '{fileName}': {e}" + Style.RESET_ALL)
        raise
    except Exception as e:
        print(Fore.RED + f"❌ Unexpected error while reading the file '{fileName}': {e}" + Style.RESET_ALL)
        raise

def findLambdaResources(resources):
    """
    Scans the CloudFormation resources for AWS Lambda functions.

    Args:
        resources (dict): The CloudFormation resources.

    Returns:
        dict: A dictionary with Lambda functions' resource names and their initial statuses.
    """
    print(Fore.CYAN + "🔍 Scanning resources for AWS Lambda functions..." + Style.RESET_ALL)
    
    dict_to_check = {}
    try:
        for i in resources:
            if resources[i].get("Type") == "AWS::Lambda::Function":
                dict_to_check[i] = {"status": "CodeNotFormatted"}
        
        if dict_to_check:
            print(Fore.GREEN + f"✅ Found {len(dict_to_check)} Lambda function(s) to check." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "⚠️ No AWS Lambda functions found in the resources." + Style.RESET_ALL)
        
        return dict_to_check
    except KeyError as e:
        print(Fore.RED + f"❌ Error: Missing expected key in resources: {e}" + Style.RESET_ALL)
        raise
    except Exception as e:
        print(Fore.RED + f"❌ Unexpected error while scanning resources: {e}" + Style.RESET_ALL)
        raise



def extractLambdaCode(resources, dict_to_check, args=None):
    """
    Processes Lambda resources and checks their inline code for syntax errors using flake8.

    Args:
        resources (dict): Dictionary containing resource definitions.
        dict_to_check (dict): Dictionary of resources to check.
        args (str): Template dictionary (not used directly in this function).

    Returns:
        dict: Updated dict_to_check with linting results.
    """
    if not isinstance(resources, dict):
        raise ValueError("Expected 'resources' to be a dictionary.")
    if not isinstance(dict_to_check, dict):
        raise ValueError("Expected 'dict_to_check' to be a dictionary.")
    
    for i in dict_to_check:
        try:
            if "ZipFile" not in resources[i]["Properties"]["Code"]:
                raise KeyError(f"'ZipFile' key missing in resource '{i}' code properties.")
            
            lambda_code = resources[i]["Properties"]["Code"]["ZipFile"]
            programming_lang = resources[i]["Properties"]["Runtime"]
            if not isinstance(lambda_code, str):
                raise ValueError(f"Expected a string for 'ZipFile' content in resource '{i}', got {type(lambda_code)}.")

            print(Fore.CYAN + f"🔍 Checking resource '{i}' for code linting..." + Style.RESET_ALL)
            if "python" in programming_lang:
                if args is None:
                    process = subprocess.Popen(
                        ['python', '-m', 'flake8', "-"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )
                else:
                    process = subprocess.Popen(
                        ['python', '-m', 'flake8', "-"] + args.split(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )
            stdout, stderr = process.communicate(input=lambda_code.encode())

            if process.returncode not in [0, 1]:  # 0: No issues, 1: Linting errors
                raise RuntimeError(f"❌ flake8 process failed with return code {process.returncode}: {stderr.decode()}")

            dict_to_check[i] = {
                "status": "FoundNoErrors" if stdout.decode() == "" else "FoundErrors",
                "errors": stdout.decode()
            }
            print(Fore.GREEN + f"✅ Linting check completed for resource '{i}'" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"❌ Error processing resource '{i}': {e}" + Style.RESET_ALL)
            raise e

    return dict_to_check


def outputPrinting(error_dict):
    """
    Prints the results of lambda function error checks with color-coded output.
    
    Args:
        error_dict (dict): A dictionary containing resources and their linting statuses.

    Returns:
        bool: True if no errors were found in any resource, False otherwise.
    """
    lst = []
    resource_count = 1
    for i in error_dict:
        if error_dict[i]["status"] == "FoundErrors":
            print(Fore.CYAN + "\n  ❌ " + str(resource_count) + f". Resource {i} has the following errors in the lambda function:\n" + Style.RESET_ALL)
            error_count = 1
            for error in error_dict[i]["errors"].split("\n")[:-1]:
                print(Fore.YELLOW + f"\t{error_count}. " + Fore.RED + error + Style.RESET_ALL)
                error_count += 1
            lst.append(False)
        elif error_dict[i]["status"] == "FoundNoErrors":
            print(Fore.GREEN + "\n  ✅ " + str(resource_count) + f". Resource {i} has no errors in the lambda function. 🎉" + Style.RESET_ALL)
            lst.append(True)
        resource_count += 1

    if all(lst) == True:
        return True
    else:
        return False


def linter(fileName, args=None):
    """
    Lint a given CloudFormation template file, checking lambda code for errors.
    
    Args:
        fileName (str): The name of the file to process and lint.
        args(str): Args you want to pass to the lint
    """
    print(Fore.WHITE + Style.BRIGHT + f"\n📝 Processing file: {fileName}" + Style.RESET_ALL)
    
    # Read the file and parse the template
    try:
        template = readFile(fileName)
        resources = template["Resources"]
        dict_to_check = findLambdaResources(resources)
        print(Fore.CYAN + f"📂 Found {len(dict_to_check)} resources to check." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"❌ Error while reading or parsing file: {e}" + Style.RESET_ALL)
        sys.exit(1)

    # Extract and lint Lambda code
    try:
        if args is None:
            error_dict = extractLambdaCode(resources, dict_to_check, args=None)
        else:
            error_dict = extractLambdaCode(resources, dict_to_check, args)
    except Exception as e:
        print(Fore.RED + f"❌ Error during Lambda code extraction: {e}" + Style.RESET_ALL)
        sys.exit(1)

    # Print output and provide final status
    if outputPrinting(error_dict):
        print(Fore.GREEN + Style.BRIGHT + "✅ No errors found in any Lambda function!" + Style.RESET_ALL)
        sys.exit(0)
    else:
        print(Fore.RED + Style.BRIGHT + "❌ Please fix the errors listed above and run the linter again." + Style.RESET_ALL)
        sys.exit(1)
