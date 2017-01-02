# todoist-tracker

This project is intended to make it easy to track various metrics for todoist,
including things like:

* how many tasks are currently OVERDUE (including today)
* how much time is allocated to currently OVERDUE (including today) tasks
* the priority level of currently OVERDUE (including today) tasks

`todoist-tracker` is a hack to make it easy to quickly gauge how "underwater"
you are and how productive you've been. It is intended to be set up as a
cronjob with a crontab entry like:

```
45 21 * * * todoist-tracker overdue n
45 21 * * * todoist-tracker overdue time
45 21 * * * todoist-tracker overdue priority
```

which runs `todoist-tracker` every night at 9:45 p.m. By default, the resulting
metrics are stored in a google spreadsheet for subsequent analysis.  Depending
on the version of `requests` that is installed via python dependencies, you may
also want to use `PYTHONWARNINGS=ignore` somewhere in your crontab to avoid
being sent warnings every time the script is run.

## quick start

1. install `todoist-tracker` from pypi:
    ```sh
    pip install todoist-tracker
    ```

1. get your todoist api token from the todoist `Settings` > `Account` > `API
   token`.

1. place your todoist api token in a `todoist.json` file in the repository root
   that looks like this:
   ```json
   {
       "token": "your-token"
   }
   ```

1. get your google spreadsheet credentials from TKTK

1. place your google spreadsheet credentials in a `google.json` file in the
   repository root that looks like this:
   ```json
   {
       "TKTK": "TKTK"
   }
   ```

1. :boom: For usage instructions, see
  ```sh
  todoist-tracker -h
  ```

## development

1. instantiate virtual environment
    ```sh
    mkvirtualenv todoist-tracker
    pip install -r requirements/python-dev
    ```

1. add the `bin/` directory to your virtualenv `PATH` and the
  project root to your `PYTHONPATH` with
  ```sh
  # setup paths on virtualenv activation
  echo 'export __PATH_TODOIST_TRACKER=$PATH' > ~/.virtualenvs/todoist-tracker/bin/postactivate
  echo 'export PATH=$PATH:'`pwd`'/bin' >> ~/.virtualenvs/todoist-tracker/bin/postactivate
  echo 'export PYTHONPATH=$PYTHONPATH:'`pwd` >> ~/.virtualenvs/todoist-tracker/bin/postactivate

  # setup paths on virtualenv deactivation
  echo 'unset PYTHONPATH' > ~/.virtualenvs/todoist-tracker/bin/predeactivate
  echo 'export PATH=$__PATH_TODOIST_TRACKER' > ~/.virtualenvs/todoist-tracker/bin/predeactivate
  ```

1. follow the quick start instructions above to get your todoist credentials.
