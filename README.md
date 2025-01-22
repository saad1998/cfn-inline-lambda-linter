# 🚀 cfn-inline-lambda-linter  

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cfn-inline-lambda-linter)](https://pypi.org/project/cfn-inline-lambda-linter/)  
[![PyPI](https://img.shields.io/pypi/v/cfn-inline-lambda-linter)](https://pypi.org/project/cfn-inline-lambda-linter/)  
[![License](https://img.shields.io/github/license/saad1998/cfn-inline-lambda-linter)](./LICENSE)  
[![Code Coverage](https://img.shields.io/codecov/c/github/saad1998/cfn-inline-lambda-linter)](https://codecov.io/gh/saad1998/cfn-inline-lambda-linter)  
[![GitHub Stars](https://img.shields.io/github/stars/saad1998/cfn-inline-lambda-linter)](https://github.com/saad1998/cfn-inline-lambda-linter/stargazers)  

**`cfn-inline-lambda-linter`** is a powerful and lightweight tool for **linting inline Lambda functions** embedded in AWS CloudFormation templates. Optimize your Lambda code, catch potential issues, and enforce best practices effortlessly.  

## ✨ Features  

🔍 **Automatic Detection**: Scans YAML/JSON templates to identify inline Lambda functions.  
⚡ **Lightning-Fast Linting**: Validates syntax, enforces standards, and identifies anti-patterns.  
🛠 **Customizable Rules**: Extend with your own linting rules to suit your project needs.  
📦 **CI/CD Ready**: Seamlessly integrate into any CI/CD pipeline.  
📈 **Future-Proof**: Built with extensibility and AWS updates in mind.  

## 🛠 Installation  

Install via [pip](https://pip.pypa.io/):  

```bash  
pip install cfn-inline-lambda-linter
```

Or Install the latest development version:

```bash
pip install git+https://github.com/saad1998/cfn-inline-lambda-linter.git  
```
## 🚀 Quick Start

### Lint a CloudFormation Template

```bash
cfn-inline-lambda-linter template.yaml
```

### Pass args to Lint

```bash
cfn-inline-lambda-linter template.yaml --args "--max-line-length=88 --ignore=E203,W503"
```

### 🎣 Pre-Commit Hook Integration

Ensure your code is always clean and adheres to best practices by integrating `cfn-inline-lambda-linter` as a **pre-commit hook**!

#### Why Use This Hook?

- **Automatic linting**: Detect and resolve CloudFormation template issues effortlessly.
- **Error prevention**: Catch inline Lambda errors before deployment.
- **Productivity boost**: Spend less time debugging and more time building.

#### Setting Up the Pre-Commit Hook

1. Install `pre-commit` globally (if not already installed):

   ```bash
   pip install pre-commit
   ```

2. Add the following to your project's `.pre-commit-config.yaml` file:

   ```yaml
   repos:
     - repo: https://github.com/saad1998/cfn-inline-lambda-linter
       rev: v0.1.0  # Replace with the latest version
       hooks:
         - id: cfn-inline-lambda-linter
           files: template.yaml
   ```

3. Install the pre-commit hook in your local repository:

   ```bash
   pre-commit install
   ```

4. Test it by running pre-commit on all files:

   ```bash
   pre-commit run --all-files
   ```

#### How It Works

Once the hook is configured, every time you try to commit changes:

- The hook will automatically scan your CloudFormation templates containing inline Lambda code.
- Errors or warnings will be highlighted, ensuring only high-quality configurations are committed.

#### Customize the Hook

You can pass arguments to the hook by modifying `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/your-username/cfn-inline-lambda-linter
    rev: v0.1.0
    hooks:
      - id: cfn-inline-lambda-linter
        files: template.yaml
        args: ["--args=--max-line-length=88  --ignore=E203,W503"]
```

#### 🎉 You're All Set!

Your project is now equipped with an automated linter that ensures CloudFormation templates and inline Lambda code are always error-free before committing.

## 🌟 Why Choose Us?
* **Developer-Friendly**: Clean output with actionable messages.
* **AWS Focused**: Tailored specifically for AWS Lambda in CloudFormation.
* **Open Source**: Free forever, with a growing community of contributors.

## 🤝 Contributing

We ❤️ contributions!
But at the moment it has been paused.
It will be resumed when we have published our Contributing.md guide.

## 🗺 Roadmap
✅ Add support for nested templates.
✅ Add linting support for lambda functions written in other languages.
🚧 Advanced static analysis for Lambda functions.
🔜 Enhanced logging for CI/CD pipelines.

## 📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 🎉 Show Your Support
Give a ⭐ if this project helps you improve your CloudFormation workflows!

## 📧 Contact
Got questions or suggestions? Open an issue here.

"Code smarter, not harder!"
