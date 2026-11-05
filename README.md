# Service Health Monitor

A small project to practice HTTP health checks with Python.

Start a local server in one terminal:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

From the repository root in another terminal:

```bash
TARGET_URL=http://localhost:8000 python3 -m app.monitor
```

The script prints the status, HTTP code, and response time. A 2xx response counts as up. Stop the server and try again to see down. The script prints down as data; it does not exit with an error code.
