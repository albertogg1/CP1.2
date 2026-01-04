pipeline{
    agent any
    
    stages{
        stage('Get code'){
            steps{
                // Obtener el código fuente desde el repositorio Git
                echo 'Hello World' // Esto no es el echo del sistema operativo sino el del log de Jenkins
                git branch: 'feature_fix_coverage', url: 'https://github.com/albertogg1/CP1.2.git'
                bat 'dir'
                bat 'echo %WORKSPACE%'
            }
        }
        
        stage('Unit'){
            steps{
                catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                     bat '''
                        set PYTHONPATH=%WORKSPACE%
                        coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest --junitxml=result-unit.xml test\\unit
                    '''
                    junit 'result-unit.xml'
                }
            }
        }

        stage('Rest'){
            steps{
                bat '''
                    set FLASK_APP=app\\api.py
                    start flask run
                    start java -jar C:\\EU_DevOps_Cloud\\ejercicios\\wiremock-standalone-3.13.2.jar --port 9090 --root-dir test\\wiremock
                    
                    ping -n 10 127.0.0.1

                    set PYTHONPATH=%WORKSPACE%
                    pytest --junitxml=result-rest.xml test\\rest
                '''
                junit 'result-rest.xml'
            }
        }   

        stage('Static'){
            steps{
                    bat '''
                        set PYTHONPATH=%WORKSPACE%
                        flake8 --exit-zero --format=pylint --max-line-length 90 app >flake8.out
                    '''
                    recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')], qualityGates: [[threshold: 8, type: 'TOTAL', unstable: true], [threshold: 10, type: 'TOTAL', unstable: false]]
            }
        }

        stage('Security'){
            steps{
                bat '''
                    set PYTHONPATH=%WORKSPACE%
                    bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}" 
                '''
                recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], qualityGates: [[threshold: 2, type: 'TOTAL', unstable: true], [threshold: 4, type: 'TOTAL', unstable: false]]
            }
        }

        stage('Performance'){
            steps{
                bat '''
                    set FLASK_APP=app\\api.py
                    start flask run

                    ping -n 10 127.0.0.1

                    C:\\EU_DevOps_Cloud\\ejercicios\\apache-jmeter-5.6.3\\bin\\jmeter.bat -n -t test\\jmeter\\flask.jmx -l flask.jtl
                '''
                perfReport sourceDataFiles: 'flask.jtl'
            }
        }
 
        stage('Coverage'){
            steps{
                bat '''
                    coverage xml
                    coverage report
                '''
                recordCoverage qualityGates: [[integerThreshold: 95, metric: 'LINE', threshold: 95.0],
                                              [criticality: 'ERROR', integerThreshold: 85, metric: 'LINE', threshold: 85.0],
                                              [integerThreshold: 90, metric: 'BRANCH', threshold: 90.0],
                                              [criticality: 'ERROR', integerThreshold: 80, metric: 'BRANCH', threshold: 80.0]],
                                tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']]
            }
        }

    } 
}