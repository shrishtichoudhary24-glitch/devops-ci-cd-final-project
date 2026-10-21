# CI/CD Capstone Project – Counter Service

Final project for the CI/CD course. A small Flask counter microservice with a complete
CI/CD setup:

- **GitHub Actions** – lint with flake8 and run unit tests with nose on every push / PR
- **Tekton** – reusable tasks (`cleanup`, `flake8`, `nose`) and a `cd-pipeline` pipeline
- **OpenShift Pipelines** – clone, lint, test, build (buildah) and deploy the app

Author: Shrishti, Vishwakarma Institute of Technology (VIT), Pune

## Project layout

```
.github/workflows/workflow.yml   GitHub Actions CI workflow
.tekton/tasks.yml                Tekton tasks: cleanup, flake8, nose
.tekton/pipeline.yml             Tekton pipeline: cd-pipeline
.tekton/pvc.yml                  PersistentVolumeClaim: oc-lab-pvc
service/                         Flask application
tests/                           Unit tests (nose)
Dockerfile                       Container image
```

## REST API

| Method | Route               | Description                  |
|--------|---------------------|------------------------------|
| GET    | `/counters`         | List all counters            |
| POST   | `/counters/<name>`  | Create a counter (starts 0)  |
| GET    | `/counters/<name>`  | Read a counter               |
| PUT    | `/counters/<name>`  | Increment a counter          |
| DELETE | `/counters/<name>`  | Delete a counter             |

## Run locally

```bash
python3.9 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask run
nosetests -v
```

## OpenShift pipeline

```bash
oc apply -f .tekton/pvc.yml
oc apply -f .tekton/tasks.yml
oc apply -f .tekton/pipeline.yml
tkn pipeline start cd-pipeline \
  -p repo-url="https://github.com/<your-username>/<repo>.git" \
  -p branch=main \
  -p build-image=image-registry.openshift-image-registry.svc:5000/$SN_ICR_NAMESPACE/tekton-lab:latest \
  -w name=pipeline-workspace,claimName=oc-lab-pvc \
  --showlog
```
