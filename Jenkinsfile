pipeline {
    agent {
        kubernetes {
            cloud 'rsys-devel'
            defaultContainer 'miniforge3'
            inheritFrom 'miniforge'
        }
    }
    stages {
        stage("install") {
            steps {
                sh 'conda config --add channels bioconda'
                sh 'conda config --add channels https://git.reslate.systems/api/packages/ydeng/conda'
                sh 'conda env update -n base -f environment.yml'
            }
        }
        stage("unit tests") {
            steps {
                sh returnStatus: true, script: "python -m pytest --junitxml=test_results.xml --cov=src --cov-report xml:coverage.xml"
                xunit checksName: '', tools: [JUnit(excludesPattern: '', pattern: 'test_results.xml', stopProcessingIfError: true)]
                recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']])
            }
        }
        stage("build") {
            steps {
                sh "python -m build"
                sh "grayskull pypi dist/*.tar.gz --maintainers 'Harrison Deng'"
                sh "python scripts/patch_recipe.py"
                sh 'conda build autobigs-cli -c bioconda --output-folder conda-bld --verify'
            }
        }
        stage("archive") {
            steps {
                archiveArtifacts artifacts: 'dist/*.tar.gz, dist/*.whl, conda-bld/**/*.conda', fingerprint: true, followSymlinks: false, onlyIfSuccessful: true
            }
        }
        stage("publish") {
            parallel {
                stage ("git.reslate.systems") {
                    when {
                        branch '**/main'
                    }

                    environment {
                        CREDS = credentials('username-password-rs-git')
                    }
                    steps {
                        sh script: 'python -m twine upload --repository-url https://git.reslate.systems/api/packages/ydeng/pypi -u ${CREDS_USR} -p ${CREDS_PSW} --non-interactive --disable-progress-bar --verbose dist/*'
                        sh 'curl --user ${CREDS_USR}:${CREDS_PSW} --upload-file conda-bld/**/*.conda https://git.reslate.systems/api/packages/${CREDS_USR}/conda/$(basename conda-bld/**/*.conda)'
                    }
                }
                stage ("pypi.org") {
                    when {
                        tag '*.*.*'
                    }
                    environment {
                        TOKEN = credentials('pypi.org')
                    }
                    steps {
                        sh script: 'python -m twine upload -u __token__ -p ${TOKEN} --non-interactive --disable-progress-bar --verbose dist/*'
                    }
                }
            }
        }
    }
}