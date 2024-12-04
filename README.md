# Stock-Backtesting

## instructions

```sh
$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
$ python3 mainwindow.py
$ deactivate
```

## testing

```sh
$ python3 -m unittest test.py
$ python3 -m unittest integration_test.py
```

# mvc architecture (by file)
## model
- strategy.py
- *.json
- *.csv
## view
- mainwindow_ui.py
- backtest_ui.py
- mpl_canvas.py
- plot_utils.py
- *.ui
## controller
- main.py

# testing
- test.py
- integration_test.py
- algos.py