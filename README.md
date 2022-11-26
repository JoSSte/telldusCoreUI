# telldusCoreUI
PHP frontent to Telldus tdtool utility with Python based backend, since there is no PHP API. if database connection is lost, a local sqlite database is populated.

## Running
Ensure that `telldusd` service is running. (Verify with `tdtool --list`)  

## Python Callback handler
This it the backend service registering events sent to the telldus device by the temperature sensors and buttons  

### Installing Prerequisites
`python -m pip install -r requirements.txt`  

### Configuring
Put your database connection details in `.env`