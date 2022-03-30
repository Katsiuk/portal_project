pipeline {
    agent any
    stages {
        stage('Preparation') {
            steps {
                echo 'Creating a directory'
                sh 'mkdir -p build'
                
                echo 'Cloning files from (branch "' + env.BRANCH_NAME + '" )'
                dir('build') {
                    git branch: 'main', credentialsId: 'git_jenkins_portal', url: 'git@github.com:Katsiuk/portal_project.git'
                }
            }
        }
        stage('Build') {
            steps {
                
            }
        }
    }
}
