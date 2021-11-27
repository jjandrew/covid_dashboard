import pylint.lint
pylint_opts = ['covid_data_handler.py', 'covid_news_handling.py']
pylint.lint.Run(pylint_opts)
