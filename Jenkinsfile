pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install --user -q yfinance pyyaml tabulate pandas matplotlib numpy || true'
            }
        }
        stage('Run Stock Analysis') {
            steps {
                sh 'bash stock.sh'
            }
        }
    }

    post {
        success {
            echo 'Stock analysis pipeline completed successfully!'
        }
        failure {
            echo 'Stock analysis pipeline failed!'
        }
    }
}
