pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"C:\\Users\\Dhruv\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pip install --upgrade pip'
                bat '"C:\\Users\\Dhruv\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"C:\\Users\\Dhruv\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pytest -v'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t inventory-backend:latest .'
            }
        }

        stage('Docker Hub Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials-new',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )]) {

                    bat 'echo Jenkins Docker username: %DOCKERHUB_USERNAME%'

                    powershell '''
                    $env:DOCKERHUB_PASSWORD | docker login -u $env:DOCKERHUB_USERNAME --password-stdin
                    '''

                    bat 'docker tag inventory-backend:latest %DOCKERHUB_USERNAME%/inventory-management:latest'

                    bat 'docker push %DOCKERHUB_USERNAME%/inventory-management:latest'

                    bat 'docker logout'
                }
            }
        }
    }

    post {
        success {
            echo 'Inventory Management CI/CD completed successfully!'
        }

        failure {
            echo 'Inventory Management CI/CD failed!'
        }
    }
}