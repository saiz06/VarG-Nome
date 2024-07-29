pipeline {
    agent any

    environment {
         SONARQUBE_DASHBOARD_URL = "https://sonarqube.cafevariome.org/dashboard?id=uol_similarity_service"
         PYTHON_VERSION = '3.10'
         NVD_API_KEY = credentials('nvd-api-key')
    }

    stages {
        // Checkout code
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'AdminGitJenkins', url: 'git@github.com:CafeVariomeUoL/SimilarityService.git'
            }
        }
        // Execute OWASP Dependency check
        stage('OWASP Dependency Check') {
            steps {
                sh '''
                    /local/jenkins_home/tools/org.jenkinsci.plugins.DependencyCheck.tools.DependencyCheckInstallation/OWASP-DP-Check/bin/dependency-check.sh --project "${JOB_NAME}" --enableExperimental --scan . --format HTML --format XML --format JSON --nvdApiKey $NVD_API_KEY
                '''
            }
        }

        stage('Set up Python env and Run Coverage Tests') {
            steps {
                script {
                    try{
                        sh '''
                        source /local/software/anaconda3/etc/profile.d/conda.sh
                        conda activate envpy310
                        pip install -r requirements.txt
                        pip install pytest-cov
                        pytest --cov=./ --cov-report=xml:coverage.xml
                    '''
                    } catch (Exception e){
                        currentBuild.result = 'UNSTABLE'
                        echo 'Test execution failed, but coverage report will be published.'
                        echo e.getMessage()
                    }

                }
            }
        }
        stage('Publish Coverage Results'){
            steps{
                cobertura(coberturaReportFile: '**/coverage.xml')
            }
        }
        // Execute SonarQube analysis
        stage('SonarQube Analysis - Similarity Service') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        /local/jenkins_home/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQube_Scanner/bin/sonar-scanner \
                         -Dsonar.projectKey=uol_similarity_service \
                         -Dsonar.projectName='SimilarityService' \
                         -Dsonar.sources=. \
                         -Dsonar.python.version=${PYTHON_VERSION} \
                         -Dsonar.python.coverage.reportPaths=coverage.xml \
                         -Dsonar.exclusions=**/dependency-check-report.xml,**/dependency-check-report.html \
                         -Dsonar.dependencyCheck.jsonReportPath=${WORKSPACE}/dependency-check-report.json
                    '''
                }
                script{
                    def qg = waitForQualityGate()
                    SONARQUBE_RESULT = qg.status
                }
            }
        }
    }

    post {
        always {
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            cleanWs()
        }
        success {
            sendSlackNotifications('SUCCESS', 'good', SONARQUBE_RESULT)
        }
        unstable {
            sendSlackNotifications('FAILURE', 'warning', SONARQUBE_RESULT)
        }
        failure {
           sendSlackNotifications('FAILURE', 'danger', SONARQUBE_RESULT)
        }
    }
} // pipeline closing

// Send slack notifications
def sendSlackNotifications(String status, String color, String sonarQubeResult){
    script {
        def sonarStatusMsg = sonarQubeResult == 'OK' ? 'Passed' : "Failed (${sonarQubeResult})"
        slackSend(
            tokenCredentialId: 'slack-jenkins-integration',
            channel: '#cv3-job-alerts',
            message: "${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL}). SonarQube QualityGate status: ${sonarStatusMsg}.  View SonarQube dashboard for results: ${env.SONARQUBE_DASHBOARD_URL}",
            color: color
        )
    }
}