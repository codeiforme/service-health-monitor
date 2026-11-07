# Local Kubernetes

You need Docker, kind, kubectl, and Terraform 1.9 or later below 2.0. Run these commands from the repository root. This uses a local cluster, not AWS.

```bash
docker compose down
kind create cluster --name health-monitor
docker build -t service-health-monitor:local .
kind load docker-image service-health-monitor:local --name health-monitor
terraform -chdir=terraform init
terraform -chdir=terraform fmt
terraform -chdir=terraform validate
terraform -chdir=terraform plan
```

Read the plan. It should create one namespace, two Deployments, and one Service. Terraform selects the `kind-health-monitor` context in your kubeconfig.

```bash
terraform -chdir=terraform apply
kubectl -n health-monitor get pods
kubectl -n health-monitor logs deployment/monitor
bash scripts/kubernetes-demo.sh down
```

Wait for the target to become not ready and for the monitor to report down. Readiness checks `/health`; liveness checks `/live`. The failure marker affects readiness only. The Service may stop forwarding traffic, so the monitor may see a connection error instead of HTTP 503.

```bash
bash scripts/kubernetes-demo.sh up
kubectl -n health-monitor get pods
kubectl -n health-monitor logs deployment/monitor
```

Wait for an up check. Keep the generated `.terraform.lock.hcl` in Git. State files stay local and are ignored.

If you change the code, build and load a new tag, then apply with `-var='image=service-health-monitor:v2'`. Keep that image value on later plans too. Terraform does not build images or create the cluster. n8n stays in the separate Compose demo.

When finished, remove the Terraform resources before deleting the cluster:

```bash
terraform -chdir=terraform destroy
kind delete cluster --name health-monitor
```
