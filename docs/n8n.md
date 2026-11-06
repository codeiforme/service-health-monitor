# n8n

Start n8n with `docker compose up -d n8n`, then open http://localhost:5678 and create the local account.

Import `n8n/health-events.json`. The Webhook node receives the check. The Edit Fields node keeps the target, status, and timestamp. Publish or activate the workflow.

Create a `.env` file in the repository root:

```dotenv
WEBHOOK_URL=http://n8n:5678/webhook/service-health
```

Use this production webhook path, not `/webhook-test/`. The monitor uses `n8n` as the hostname because it runs in another container.

```bash
docker compose up -d --force-recreate monitor
bash scripts/demo.sh down
```

Wait for a down execution in n8n before running `bash scripts/demo.sh up`. Then check for an up execution. The first check also sends an event.

If the webhook fails, the monitor tries again on the next check. The webhook replies before the rest of the workflow finishes, so inspect the execution result too. Events are kept in execution history, which may be pruned; this is not a permanent incident database.

The local webhook has no authentication. Keep this demo private. `docker compose down` keeps the n8n volume; adding `-v` deletes its account, workflow, and history. The Compose file pins an example n8n image version; review the supported release before using it outside this local exercise.
