# Service Health Monitor

A small Python monitor that checks a web service and prints its status and response time.

## Run

You need Docker with Compose, Bash, and curl. Run commands from the repository root.

```bash
docker compose up -d --build target monitor
docker compose logs -f monitor
```

Leave the log view with Ctrl+C. The containers keep running. Checks run about every 10 seconds.

## Try a failure

```bash
bash scripts/demo.sh down
curl -i http://localhost:8000/health
```

Wait for a down check. Then restore the service:

```bash
bash scripts/demo.sh up
docker compose logs --tail=10 monitor
```

Wait for up. Use `docker compose down` to stop the project. The failure is simulated with a marker file.

## Tests

With Python 3.12, run `bash scripts/check.sh`. These tests simulate HTTP responses and errors. Use the demo above to check real behavior.
