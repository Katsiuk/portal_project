pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo "---------------Build Started---------------"
                echo 'Creating a directory'
                sh 'mkdir -p build'
                
                echo 'Cloning files from Github...'
                dir('build') {
                    git branch: 'main', credentialsId: 'git_jenkins_portal', url: 'git@github.com:Katsiuk/portal_project.git'
                }
                echo "---------------Build Finished---------------"
            }
        }
        stage ("Test") {
            steps {
                echo "---------------Test Started---------------"
                sh '''
                    PYVERSION=$(python3 --version)
                    if [[ -z "$PYVERSION" ]]
                    then
                        echo "No Python!"
                    else
                        echo "Hello from $PYVERSION!"
                    fi
                '''
                echo "---------------Test Finished---------------"
            }
        }
         stage('Deploy') {
            steps {
                sshPublisher(publishers: [sshPublisherDesc(configName: 'test_server', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'cd build; sudo apt install -y python3 python3-pip python3-venv; python3 -m venv env; source env/bin/activate; pip3 install -r requirements.txt; python3 __init__.py', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '**/*')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
                sshPublisher(publishers: [sshPublisherDesc(configName: 'node_1', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'cd build; sudo apt install -y python3 python3-pip python3-venv; python3 -m venv env; source env/bin/activate; pip3 install -r requirements.txt; python3 __init__.py', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '**/*')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false), sshPublisherDesc(configName: 'node_2', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'cd build; sudo apt install -y python3 python3-pip python3-venv; python3 -m venv env; source env/bin/activate; pip3 install -r requirements.txt; python3 __init__.py', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '**/*')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
            }
        }
    }
}
