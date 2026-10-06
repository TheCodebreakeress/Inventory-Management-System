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
                withCredentials([string(
                    credentialsId: 'dockerhub-token',
                    variable: 'DOCKERHUB_TOKEN'
                )]) {

                    powershell '''
                    $env:DOCKERHUB_TOKEN | docker login -u jill0410 --password-stdin
                    '''

                    bat 'docker tag inventory-backend:latest jill0410/inventory-management:latest'

                    bat 'docker push jill0410/inventory-management:latest'

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