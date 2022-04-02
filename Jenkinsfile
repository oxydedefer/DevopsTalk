pipeline {
    agent any

    stages {
        stage('VCS') {
            steps {
                git branch: 'develop', url: 'https://github.com/oxydedefer/DevopsTalk.git'
            }
        }
        
        stage('Build') {
            steps {
               sh 'docker build -f Dockerfile.python.ci -t talk-devops-app-build:latest .'
            }
        }
        stage('Testing') {
             parallel {
                stage('unit-test') {
                    steps {
                       sh 'docker run --rm -i talk-devops-app-build:latest python sample-test.py'
                    }
                }
                stage('Code analysis Sonarqube') {
                    steps {
                       sh """ docker run --rm -i talk-devops-app-build:latest /sonar-scanner/bin/sonar-scanner \
                                -Dsonar.projectKey=devops-talk \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=http://192.168.1.142:9000 \
                                -Dsonar.login=145320bcea88d369d3e027c16417fee59895bfdd"""
                    }
                }
             }
        }
        stage('Clean build image') {
            steps {
               sh 'docker image rm talk-devops-app-build:latest'
            }
        }
        stage('Build & Deploy release images') {
            steps {
               sh 'docker build -f Dockerfile.flask -t talk-devops-app:latest .'
            }
            steps {
               docker tag talk-devops-app:latest registry.heroku.com/devops-talk/web  
               withCredentials([string(credentialsId: 'HEROKU_API_KEY', variable: 'HEROKU_API_KEY_SECRET')]) {      
                    HEROKU_API_KEY=${HEROKU_API_KEY_SECRET} heroku container:login
                    docker push registry.heroku.com/devops-talk/web
                    HEROKU_API_KEY=${HEROKU_API_KEY_SECRET} heroku container:release web --app devops-talk
                } 
    
            }
        }

    }
    
}