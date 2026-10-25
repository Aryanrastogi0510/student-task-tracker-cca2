pipeline {
    agent any
    options { timestamps(); disableConcurrentBuilds() }
    environment {
        IMAGE_NAME = 'aryan05102005/student-task-tracker'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build and Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements-dev.txt
                    python -m compileall -q app.py tests
                    pytest -q
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                '''
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${REGISTRY_CREDENTIALS}",
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh '''
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl set image deployment/student-task-tracker student-task-tracker=${IMAGE_NAME}:${BUILD_NUMBER}
                    kubectl rollout status deployment/student-task-tracker --timeout=180s
                '''
            }
        }
        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl get pods -o wide
                    kubectl get deployment student-task-tracker
                    kubectl get service student-task-tracker
                    kubectl get deployment student-task-tracker -o=jsonpath='{.spec.template.spec.containers[0].image}'
                    echo
                '''
            }
        }
    }
    post { always { echo "Pipeline finished: ${currentBuild.currentResult}" } }
}
