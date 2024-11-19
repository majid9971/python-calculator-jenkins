pipeline {
    agent any

    environment {
        SONARQUBE = 'SonarQube'  // SonarQube server name
        ARTIFACTORY = 'Artifactory'  // JFrog Artifactory server name
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-username/project-repo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                }
                dir('backend') {
                    sh 'python -m venv venv'
                    sh './venv/bin/pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('backend') {
                    sh 'python -m unittest discover'
                }
                dir('frontend') {
                    sh 'npm test -- --coverage'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('SonarQube') {
                        dir('backend') {
                            sh 'sonar-scanner'
                        }
                    }
                }
            }
        }

        stage('Build') {
            steps {
                dir('frontend') {
                    sh 'npm run build'
                }
                dir('backend') {
                    sh 'python setup.py bdist_wheel'
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: '**/build/**/*, **/dist/**/*', allowEmptyArchive: true
            }
        }

        stage('Push to Artifactory') {
            steps {
                script {
                    rtUpload(
                        serverId: 'Artifactory',
                        targetRepo: 'your-artifact-repo',
                        source: '**/build/**/*',
                        target: 'frontend/'
                    )
                    rtUpload(
                        serverId: 'Artifactory',
                        targetRepo: 'your-artifact-repo',
                        source: '**/dist/**/*',
                        target: 'backend/'
                    )
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Build successful.'
        }
        failure {
            echo 'Build failed.'
        }
    }
}
