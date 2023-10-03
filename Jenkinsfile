pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    env.VERSION = sh( script: 'git tag --contains ${GIT_COMMIT}', returnStdout: true).replace('v', '')
                }
                sh 'docker build --tag dazzler-tt:${VERSION} .'
            }
        }
        stage('Release') {
            steps {
                sh 'cosmos-release ecs-service dazzler-tt ${VERSION} myAppImage=dazzler-tt:${VERSION}'

            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                sh 'cosmos deploy-ecs dazzler-tt test'
            }
        }
    }
}
