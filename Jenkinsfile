pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    parameters {
        string(name: 'TF_STATE_BUCKET', description: 'Existing S3 bucket used for Terraform state')
        string(name: 'TF_LOCK_TABLE', defaultValue: 'restaurant-reservation-terraform-locks', description: 'DynamoDB Terraform lock table')
        string(name: 'AWS_PROFILE_NAME', defaultValue: 'prototype-new', description: 'AWS CLI profile on the Jenkins agent')
        booleanParam(name: 'DEPLOY', defaultValue: true, description: 'Apply the Terraform deployment')
    }

    environment {
        AWS_REGION = 'us-east-2'
        AWS_PROFILE = "${params.AWS_PROFILE_NAME}"
        TF_IN_AUTOMATION = 'true'
    }

    stages {
        stage('Metadata') {
            steps {
                script {
                    env.IMAGE_TAG = sh(script: 'git rev-parse --short=12 HEAD', returnStdout: true).trim()
                    env.AWS_ACCOUNT_ID = sh(script: 'aws sts get-caller-identity --query Account --output text', returnStdout: true).trim()
                    env.ECR_REGISTRY = "${env.AWS_ACCOUNT_ID}.dkr.ecr.${env.AWS_REGION}.amazonaws.com"
                    env.BACKEND_IMAGE = "${env.ECR_REGISTRY}/restaurant-reservation-backend:${env.IMAGE_TAG}"
                    env.FRONTEND_IMAGE = "${env.ECR_REGISTRY}/restaurant-reservation-frontend:${env.IMAGE_TAG}"
                }
            }
        }

        stage('Test') {
            parallel {
                stage('Backend') {
                    steps {
                        sh '''
                            docker build -t restaurant-reservation-backend:test backend
                            docker run --rm \
                              -e DATABASE_URL=sqlite:////tmp/test.db \
                              -v "$WORKSPACE/backend/tests:/app/tests:ro" \
                              restaurant-reservation-backend:test \
                              python -m pytest -q tests
                        '''
                    }
                }
                stage('Frontend') {
                    steps {
                        dir('frontend') {
                            sh 'npm ci'
                            sh 'CI=true npm test -- --watchAll=false'
                        }
                    }
                }
                stage('Terraform') {
                    steps {
                        dir('deployment') {
                            sh 'terraform fmt -check -recursive'
                        }
                    }
                }
            }
        }

        stage('Build Images') {
            steps {
                sh 'docker build --platform linux/amd64 -t "$BACKEND_IMAGE" backend'
                sh 'docker build --platform linux/amd64 --build-arg REACT_APP_API_BASE_URL=/api -t "$FRONTEND_IMAGE" frontend'
            }
        }

        stage('Push Images') {
            steps {
                sh 'aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ECR_REGISTRY"'
                sh '''
                    aws ecr describe-images --repository-name restaurant-reservation-backend --image-ids "imageTag=$IMAGE_TAG" >/dev/null 2>&1 || docker push "$BACKEND_IMAGE"
                    aws ecr describe-images --repository-name restaurant-reservation-frontend --image-ids "imageTag=$IMAGE_TAG" >/dev/null 2>&1 || docker push "$FRONTEND_IMAGE"
                '''
            }
        }

        stage('Deploy') {
            when {
                expression { params.DEPLOY }
            }
            steps {
                dir('deployment') {
                    sh '''
                        terraform init -reconfigure \
                          -backend-config="bucket=$TF_STATE_BUCKET" \
                          -backend-config="key=restaurant-reservation/terraform.tfstate" \
                          -backend-config="region=$AWS_REGION" \
                          -backend-config="dynamodb_table=$TF_LOCK_TABLE"
                        terraform validate
                        terraform plan -out=tfplan -var="image_tag=$IMAGE_TAG"
                        terraform apply -auto-approve tfplan
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout "$ECR_REGISTRY" || true'
            deleteDir()
        }
    }
}
