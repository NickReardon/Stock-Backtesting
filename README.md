# Stock-Backtesting

## Setup

```sh
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
# Install the AWS CLI separately if Lambda updates are enabled.
python3 controller.py
deactivate
```

## Optional AWS Lambda price updates

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
python3 -m unittest test.py
python3 -m unittest integration_test.py
```
