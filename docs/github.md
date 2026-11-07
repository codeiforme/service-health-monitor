# GitHub

Create an empty repository named `service-health-monitor` in your GitHub account. Your local repository already has commits. Replace `YOUR_USERNAME` below:

```bash
git remote add origin https://github.com/YOUR_USERNAME/service-health-monitor.git
git push -u origin main
```

If `origin` already exists, check `git remote -v` and use that remote. Use `git push` for later commits.

Open the Actions page and check the Tests workflow. It runs Python tests, checks the Compose file, and builds the Docker image. After step 07 it also validates Terraform. Read the result before saying CI works.
