pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo "---------------Build Started---------------"
                echo 'Creating a directory'
                sh 'mkdir -p portal'
                
                echo 'Cloning files from Github...'
                dir('portal') {
                    git branch: 'main', credentialsId: 'git_jenkins_portal', url: 'git@github.com:Katsiuk/portal_project.git'
                }
                echo "---------------Build Finished---------------"
            }
        }
        stage ("Test") {
            steps {
                echo "---------------Test Started---------------"
                build 'JOB1'
                echo "---------------Test Finished---------------"
            }
        }
         stage('Deploy') {
            steps {
				sshPublisher(publishers: [sshPublisherDesc(configName: 'node_1', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'for i in $(pgrep python3); do kill -9 $i; done; cd portal; python3 -m venv env; source env/bin/activate; pip3 install -r requirements.txt; nohup python3 __init__.py  > log.txt 2>&1 &', flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '**/*')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
				sshPublisher(publishers: [sshPublisherDesc(configName: 'node_2', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'for i in $(pgrep python3); do kill -9 $i; done; cd portal; python3 -m venv env; source env/bin/activate; pip3 install -r requirements.txt; nohup python3 __init__.py  > log.txt 2>&1 &', flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '**/*')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
			}
        }
    }
}
