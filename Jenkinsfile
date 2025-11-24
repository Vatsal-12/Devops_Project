pipeline {
  agent any

  environment {
    VENV_DIR = "${WORKSPACE}/venv"
  }

  tools {
    // No special Jenkins tool config required for Python (we'll use system python)
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python venv & Install') {
      steps {
        sh '''
          python3 -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          . ${VENV_DIR}/bin/activate
          mkdir -p reports
          pytest -q --junitxml=reports/junit-results.xml
        '''
      }
      post {
        always {
          junit 'reports/junit-results.xml'
        }
      }
    }

    stage('Static Analysis (flake8)') {
      steps {
        sh '''
          . ${VENV_DIR}/bin/activate
          # run flake8 but don't fail pipeline on minor style issues (optional)
          flake8 --max-line-length=120 || true
        '''
      }
    }

    stage('Archive Artifacts') {
      steps {
        archiveArtifacts artifacts: 'reports/**', fingerprint: true
      }
    }

    // Optional SonarQube stage (requires Sonar config in Jenkins)
    stage('SonarQube Analysis') {
      when {
        expression { return params.RUN_SONAR == true || env.RUN_SONAR == 'true' }
      }
      steps {
        withSonarQubeEnv('SonarQube') {
          sh '''
            . ${VENV_DIR}/bin/activate
            sonar-scanner \
              -Dsonar.projectKey=sentiment_mid \
              -Dsonar.sources=. \
              -Dsonar.tests=tests \
              -Dsonar.python.version=3 \
              -Dsonar.junit.reportPaths=reports/junit-results.xml
          '''
        }
      }
    }
  }

  post {
    success {
      echo "Pipeline finished successfully"
    }
    failure {
      echo "Pipeline failed"
    }
  }
}
