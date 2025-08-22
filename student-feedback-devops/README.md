# Student Feedback DevOps

A tiny Flask app that stores student feedback in SQLite. It demonstrates Git, CI/CD, Docker, Configuration Management (Ansible), and Monitoring/Logging.

## Endpoints
- `/` — feedback form + recent submissions
- `/health` — health probe (returns `{"status":"ok"}`)

See `/deploy` and `.github/workflows/ci-cd.yml` for pipeline & deployment.
