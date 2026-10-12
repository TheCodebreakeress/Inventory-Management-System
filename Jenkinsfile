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
                    $ErrorActionPreference = "Continue"
                    $token = $env:DOCKERHUB_TOKEN.Trim()
                    Write-Host "Token length: $($token.Length)"

                    $token | docker login --username "jill0410" --password-stdin

                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker Hub login failed"
                    }
                '''

                    bat 'docker tag inventory-backend:latest jill0410/inventory-management:latest'

                    bat 'docker push jill0410/inventory-management:latest'

                    bat 'docker logout'
                }
            }
        }