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