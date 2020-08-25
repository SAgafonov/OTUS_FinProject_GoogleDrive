pipeline {
	agent any

	stages {
		stage('Move to working dir') {
			steps {
				sh 'cd /var/jenkins_home/workspace/finProject'
			}
		}
		stage('Create image') {
			steps {
				sh 'docker build -f Dockerfile -t my_tests .'
			}
		}
		stage('Run Tests') {
			steps {
				sh 'docker run --name tests my_tests'
			}
		}
		stage('Report') {
			steps {
				sh 'docker cp tests:/home/app/allure-report/ /var/jenkins_home/workspace/finProject/target/'
				script {
					allure ([
						includeProperties: false, 
						jdk: '',
						report: 'target/allure-results',
						results: [[path: 'target/allure-report']]
					])
				}
			}
		}
	}
}
