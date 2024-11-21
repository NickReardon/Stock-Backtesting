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
- algos.py
- strategy.py
- ~~test.py~~
- *.json
- *.csv
- download_thread.py
## view
- mainwindow_ui.py
- backtest_ui.py
- mpl_canvas.py
- plot_utils.py
- *.ui
## controller
- backtest_logic.py
- mainwindow.py
- ~~integration_test.py~~