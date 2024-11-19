
pipeline {
    agent any

    environment {
        SONARQUBE = 'SonarQube'  // Name of SonarQube server in Jenkins
        ARTIFACTORY_URL = 'https://yourjfrogurl'
        ARTIFACTORY_REPO = 'your-artifact-repo'
        ARTIFACTORY_CREDENTIALS = 'your-artifactory-credentials'  // Jenkins credentials ID for JFrog
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub repository
                git 'https://github.com/your-username/project-repo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install frontend dependencies (if React app)
                dir('frontend') {
                    sh 'npm install'
                }

                // Install backend dependencies (if Python app)
                dir('backend') {
                    sh 'python -m venv venv'
                    sh './venv/bin/pip install -r requirements.txt'
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Run unit tests (Backend Python)
                dir('backend') {
                    sh 'python -m unittest discover'
                }

                // Run frontend tests (React)
                dir('frontend') {
                    sh 'npm test -- --coverage'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // Perform SonarQube scan
                    withSonarQubeEnv('SonarQube') {
                        dir('frontend') {
                            sh 'npm run build' // Make sure to build before analysis
                        }
                        dir('backend') {
                            sh 'sonar-scanner' // This should work if SonarQube Scanner is set up
                        }
                    }
                }
            }
        }

        stage('Build Application') {
            steps {
                // Build the frontend and backend (use appropriate build tools)
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
                // Archive frontend and backend build artifacts
                archiveArtifacts artifacts: 'frontend/build/**/*, backend/dist/**/*', allowEmptyArchive: true
            }
        }

        stage('Push to JFrog Artifactory') {
            steps {
                script {
                    // Push artifacts to JFrog Artifactory
                    rtUpload(
                        serverId: 'Artifactory',
                        targetRepo: ARTIFACTORY_REPO,
                        source: 'frontend/build/*',
                        target: 'frontend/'
                    )
                    rtUpload(
                        serverId: 'Artifactory',
                        targetRepo: ARTIFACTORY_REPO,
                        source: 'backend/dist/*',
                        target: 'backend/'
                    )
                }
            }
        }
    }

    post {
        always {
            // Clean up if necessary or notify failure/success
            echo 'Build completed.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
