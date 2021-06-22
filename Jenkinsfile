pipeline {
  
    environment {

        GCP_PROJ_ID = "robotic-tide-284315"
        API_PATH = "apiFungalDisease/"
        GCP_SERV_ACCOUNT = "jenkins@robotic-tide-284315.iam.gserviceaccount.com"
        IMAGE_NAME = "vini-fungi"
        NAME_SPACE_PROD = "api-vine-fungi-prod"

    }

    agent {
        kubernetes {
            label 'pipeline'
            defaultContainer 'jnlp'
            yamlFile 'pipeline_jobs.yaml'
        }
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }  


        stage('Validate Model') {
            steps {
                container('python') {
                    sh "pip install -r validate_model/requirements.txt"
                    sh "python validate_model/validateModel.py"
                    sh "ls ${API_PATH}"
                } 
            }
        }
  
        stage('Build Image') {
            steps {
                container('gcloud') {
                    sh "gcloud config set project ${GCP_PROJ_ID}"
                    sh "gcloud auth activate-service-account ${GCP_SERV_ACCOUNT} --key-file=key-gcp.json"
                    sh "PYTHONUNBUFFERED=1 gcloud builds submit --config ${API_PATH}cloudbuild.yaml --substitutions=COMMIT_SHA=${env.GIT_COMMIT},TAG_NAME=${IMAGE_NAME},_PROJECT_ID=${GCP_PROJ_ID} ${API_PATH}"       
                } 
            }
        }

        stage('Deploy Model API') {
            input {
                message "Do you want to deploy in production?"
                ok "Yes"
                submitter env.BUILD_USER
            } 
     
            steps {
                container('kubectl') {
                    
                    sh "sed -i 's#NAMESPACE#${NAME_SPACE_PROD}#g' ${API_PATH}k8s-artifacts/*"
                    sh "sed -i 's#PROJECT_ID#${GCP_PROJ_ID}#g' ${API_PATH}k8s-artifacts/*"
                    sh "sed -i 's#IMAGE_NAME#${IMAGE_NAME}#g' ${API_PATH}k8s-artifacts/*"
                    sh "sed -i 's#VERSION#${env.GIT_COMMIT}#g' ${API_PATH}k8s-artifacts/*"
                    
                    sh "${API_PATH}k8s-artifacts/verify_ns_prod.sh"
                    sh "${API_PATH}k8s-artifacts/verify_secret.sh"          
                    sh "kubectl apply -n ${NAME_SPACE_PROD} -f ${API_PATH}k8s-artifacts/" 
                } 
            }
        }

    }

}

  