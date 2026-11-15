# Stock-Backtesting

## Setup

Run these commands from the repository root. CI uses Python 3.12. The Windows commands below use Python 3.14.

### Windows (PowerShell)

```powershell
py -3.14 -m venv env
.\env\Scripts\python.exe -m pip install -r requirements.txt
.\env\Scripts\python.exe controller.py
```

### Linux

```sh
python3 -m venv env
./env/bin/python -m pip install -r requirements.txt
./env/bin/python controller.py
```

For later launches, run only the last command for your platform from the repository root.

## Optional AWS Lambda price updates

Install the AWS CLI separately if Lambda updates are enabled.

AWS-backed live price deltas are disabled by default. To enable them, use
short-lived credentials from AWS IAM Identity Center, an assumed role, or an
attached workload role. Do not put AWS credentials in this repository, an
`.env` file, or a chat message.

Configure an SSO/profile outside the repository, then set the profile and
application settings in your shell:

```sh
aws configure sso --profile backtesting
aws sso login --profile backtesting
export AWS_PROFILE=backtesting
export BACKTEST_ENABLE_LAMBDA=1
export BACKTEST_AWS_REGION=us-east-1
export BACKTEST_LAMBDA_FUNCTION_NAME=getPriceDelta
```

On PowerShell, use `$env:AWS_PROFILE`, `$env:BACKTEST_ENABLE_LAMBDA`,
`$env:BACKTEST_AWS_REGION`, and `$env:BACKTEST_LAMBDA_FUNCTION_NAME`
instead of `export`.

The Lambda execution policy should allow only the required
`lambda:InvokeFunction` permission for the configured function.

## Testing

```sh
python -m unittest discover -s Test -p "test*.py" -v
```
