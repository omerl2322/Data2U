# Gunicorn configuration file
# -----------------------------------------------------------------------------------------------------
# the url for the webserver
bind = '0.0.0.0:8000'
# The maximum number of pending connections.
backlog = 2048
# The number of worker processes for handling requests.
workers = 4
# The maximum number of simultaneous clients
worker_connections = 1000
# Workers silent for more than this many seconds are killed and restarted.
timeout = 1000
# The number of seconds to wait for requests on a Keep-Alive connection.
keepalive = 2
daemon = False
# Restart workers when code changes.
reload = True
# Load application code before the worker processes are forked.
preload = True


