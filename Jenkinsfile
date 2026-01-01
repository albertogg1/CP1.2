pipeline{
    agent any
    
    stages{
        stage('Get code'){
            steps{
                // Obtener el código fuente desde el repositorio Git
                echo 'Hello World' // Esto no es el echo del sistema operativo sino el del log de Jenkins
                git branch: 'develop', url: 'https://github.com/albertogg1/CP1.2.git'
                bat 'dir'
                bat 'echo %WORKSPACE%'
            }
        }
        
        stage('Build'){
            steps{
                bat 'echo "Esto es Python, no hay nada que compilar"'
            }
        }
        
        stage('Tests'){
            parallel{
                stage('Unit'){
                    steps{
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE'){
                            bat '''
                                set PYTHONPATH=%WORKSPACE%
                                pytest --junitxml=test\\unit\\report.xml test\\unit
                            '''
                        }
                    }
                }

                stage('Service'){
                    steps{
                        bat '''
                            set FLASK_APP=app\\api.py
                            start flask run
                            start java -jar C:\\EU_DevOps_Cloud\\ejercicios\\wiremock-standalone-3.13.2.jar --port 9090 --root-dir test\\wiremock

                            echo Esperando a Flask...
                            :wait_flask
                            curl -s http://localhost:5000 >nul 2>&1 || (
                                timeout /t 2 >nul
                                goto wait_flask
                            )

                            echo Esperando a WireMock...
                            :wait_wiremock
                            curl -s http://localhost:9090 >nul 2>&1 || (
                                timeout /t 2 >nul
                                goto wait_wiremock
                            )

                            set PYTHONPATH=%WORKSPACE%
                            pytest --junitxml=result-rest.xml test\\rest
                        '''
                    }
                }   
            }
        }
 

        stage('Cobertura'){
            steps{
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE'){
                    bat '''
                        set PYTHONPATH=%WORKSPACE%
                        coverage run --source=app --omit=app\\__init__.py,app\\api.py -m pytest test\\unit
                        coverage xml
                    '''
                    recordCoverage qualityGates: [[criticality: 'NOTE', integerThreshold: 85, metric: 'LINE', threshold: 85.0], [criticality: 'ERROR', integerThreshold: 60, metric: 'LINE', threshold: 60.0]], tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']]
                }
            }
        }

        stage('Results'){
            steps{
                junit 'result*.xml'
            }
        }
    }
}