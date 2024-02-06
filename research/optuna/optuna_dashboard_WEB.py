import optuna_dashboard

storage='sqlite:///db/optuna.db'
# storage='sqlite:///test_6_multi.db'
host="192.168.1.117"
# storage='test_6.db'
web = optuna_dashboard.run_server(storage, host=host)