# Student Task Tracker — CCA 2 CI/CD Project

A small Flask web app for adding study tasks and marking them complete. The main assessed work is the automated delivery pipeline.

## Architecture
GitHub → Jenkins checkout → Python syntax check + pytest → Docker build → Docker Hub push → Minikube/Kubernetes deployment → rollout verification.

## Before running the pipeline
This starter repository is a template. Replace every `DOCKERHUB_USERNAME` placeholder with your Docker Hub username, including in `Jenkinsfile` and `k8s/deployment.yaml`. Commit and push that change.

### Jenkins prerequisites
On the Jenkins agent running the job, install/configure Python 3, Docker CLI/daemon, `kubectl`, and Minikube. Ensure the Jenkins user can run Docker and has a working kubeconfig/context for Minikube. Jenkins must be able to reach the Docker daemon and cluster.

Install Jenkins Pipeline and Git plugins. Add a Jenkins username/password credential:
- ID: `dockerhub-credentials`
- Username: your Docker Hub username
- Password: a Docker Hub access token (recommended instead of account password)

Do not put secrets in source files. Configure the Jenkins job as **Pipeline script from SCM**, select Git, enter your GitHub repository URL and branch, and set script path to `Jenkinsfile`.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
python app.py
```
Open `http://127.0.0.1:5000`; health check: `http://127.0.0.1:5000/health`.

## Docker test
```bash
docker build -t student-task-tracker:local .
docker run --rm -p 5000:5000 student-task-tracker:local
```

## Minikube preparation
Start Minikube on the same host/agent where the Jenkins pipeline runs (or adapt for your lab's remote-cluster setup):
```bash
minikube start
kubectl config current-context
kubectl get nodes
```
Ensure Jenkins uses the kubeconfig that accesses this cluster. This starter assumes Minikube and Jenkins pipeline agent share a host. If they do not, adapt the setup.

## Pipeline stages
1. Checkout: fetches the configured GitHub repository.
2. Build and Test: installs dependencies, checks syntax and runs pytest.
3. Build Docker Image: builds an image tagged with the Jenkins build number and `latest`.
4. Push Image: authenticates to Docker Hub using Jenkins credentials and pushes both tags.
5. Deploy: applies Kubernetes manifests, updates the Deployment to the numbered image and waits for rollout.
6. Verify: prints pod, deployment and service state.

After the first successful run, edit the footer in `templates/index.html` from `Version 1` to `Version 2`, commit and push. Run Jenkins again and show the new deployed version.

## Access the deployed app
```bash
kubectl get pods
kubectl get deployment student-task-tracker
kubectl get service student-task-tracker
minikube service student-task-tracker --url
```
Open the URL returned by the last command. For a remote host, use SSH tunnelling or an institution-approved access method rather than exposing ports publicly without review.

## Screenshots to submit
1. GitHub repository and file structure.
2. Jenkins job configuration showing Pipeline from SCM (hide secrets).
3. Jenkins console output showing successful stages.
4. Docker Hub repository with image tags.
5. `kubectl get pods`, `kubectl get deployment`, and `kubectl get service`.
6. Application open in a browser.
7. Source change from Version 1 to Version 2 and the second successful pipeline run.

## Important notes
- This project has not been pushed to your GitHub/Docker Hub or deployed to your AWS account. Configure your own credentials and infrastructure.
- AWS EC2 costs money while running; check your lab instructions and stop resources when finished.
- Tasks are stored in memory for demonstration only; they reset on restart. A database is intentionally out of scope.
- The Kubernetes manifest assumes a public Docker Hub image. If you make the repository private, configure Kubernetes image-pull credentials.
