# Service Health Monitor

The monitor checks a local web service every 10 seconds and prints the result.

## Run

In terminal A:

```bash
mkdir -p .lab
FAILURE_FILE="$PWD/.lab/unhealthy" python3 -m app.target
```

In terminal B, from the same repository root:

```bash
CHECK_INTERVAL=2 python3 -m app.monitor
```

In terminal C, run `touch .lab/unhealthy`. Wait for a down check, then run `rm .lab/unhealthy` and wait for up. Stop the Python processes with Ctrl+C.

`TARGET_URL` changes the URL. `CHECK_INTERVAL` changes the delay after each check and must be a positive whole number. Requests use a three-second socket timeout.

The target returns HTTP 503 from `/health` when the marker exists. `/live` still returns 200. This simulates an application problem, not a real server crash.
