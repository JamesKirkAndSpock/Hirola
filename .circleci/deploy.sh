#!/usr/bin/env bash

set -o errexit
set -o pipefail

download_terraform() {
    wget https://releases.hashicorp.com/terraform/0.11.4/terraform_0.11.4_linux_amd64.zip
    unzip terraform_0.11.4_linux_amd64.zip
    chmod +x terraform
    sudo mv terraform /usr/local/bin/
}

prepare_deployment_script() {
    cd ~
    git clone -b develop https://github.com/JamesKirkAndSpock/Hirola-Deployment-Script.git
    cd ~/Hirola-Deployment-Script
    mkdir account-folder
    cd account-folder
    touch account.json

    echo ${SERVICE_ACCOUNT} > ~/Hirola-Deployment-Script/account-folder/account.json
}

check_branch(){
    re='^[0-9]+$'
    OIFS=IFS
    IFS=- read var1 var2 <<< "${CIRCLE_BRANCH}"
    echo "$var1"
    if [[ ! "$var1" =~ $re && "$CIRCLE_BRANCH" != 'develop' && "$CIRCLE_BRANCH" != 'master' ]]; then
        HOST=${DEVOPS_HOST}
        ENVIRONMENT=${DEVOPS_ENVIRONMENT}
        IP_ADDRESS=${DEVOPS_IP_ADDRESS}
        REGION=${DEVOPS_REGION}
        ZONE=${DEVOPS_ZONE}
        DATABASE_NAME=${DEVOPS_DATABASE}
    fi
    
    IFS=OIFS

    if [[ "$CIRCLE_BRANCH" == 'develop' ]]; then
        HOST=${DEVELOP_HOST}
        ENVIRONMENT=${DEVELOP_ENVIRONMENT}
        IP_ADDRESS=${DEVELOP_IP_ADDRESS}
        REGION=${DEVELOP_REGION}
        ZONE=${DEVELOP_ZONE}
    fi

    if [[ "$CIRCLE_BRANCH" == 'master' ]]; then
        HOST=${MASTER_HOST}
        ENVIRONMENT=${MASTER_ENVIRONMENT}
        IP_ADDRESS=${MASTER_IP_ADDRESS}
        REGION=${MASTER_REGION}
        ZONE=${MASTER_ZONE}
    fi
}

initialise_terraform() {
    cd ~/Hirola-Deployment-Script
    terraform init -lock=false -backend-config=bucket="${GCP_BUCKET}" -backend-config=prefix="/hirola-terraform/${ENVIRONMENT}/terraform.tfstate"
}

destroy_previous_infrastructure(){
    if [[ ! "$var1" =~ $re || "$CIRCLE_BRANCH" == 'develop' || "$CIRCLE_BRANCH" == 'master' ]]; then
        terraform destroy -lock=false -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}" -var=region="${REGION}" -var=zone="${ZONE}" -var=database_password="${DATABASE_PASSWORD}" -var=database_user="${DATABASE_USER}" -var=database_name="${DATABASE_NAME}" -var=postgres_ip="${POSTGRES_IP}" -var=environment="staging" -var=gs_bucket_name="${GS_BUCKET_NAME}" -var=gs_bucket_url="${GS_BUCKET_URL}" -var=cache_ip="${IP_ADDRESS}" -var=cache_port="${CACHE_PORT}"
    else
        terraform destroy -lock=false -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}" -var=database_password="${DATABASE_PASSWORD}" -var=database_user="${DATABASE_USER}" -var=database_name="${DATABASE_NAME}" -var=postgres_ip="${POSTGRES_IP}" -var=environment="staging" -var=gs_bucket_name="${GS_BUCKET_NAME}" -var=gs_bucket_url="${GS_BUCKET_URL}" -var=cache_ip="${IP_ADDRESS}" -var=cache_port="${CACHE_PORT}"
    fi

}

build_current_infrastructure() {
    if [[ ! "$var1" =~ $re || "$CIRCLE_BRANCH" == 'develop' || "$CIRCLE_BRANCH" == 'master' ]]; then
        terraform apply -lock=false -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}" -var=region="${REGION}" -var=zone="${ZONE}" -var=database_password="${DATABASE_PASSWORD}" -var=database_user="${DATABASE_USER}" -var=database_name="${DATABASE_NAME}" -var=postgres_ip="${POSTGRES_IP}" -var=environment="staging" -var=gs_bucket_name="${GS_BUCKET_NAME}" -var=gs_bucket_url="${GS_BUCKET_URL}" -var=cache_ip="${IP_ADDRESS}" -var=cache_port="${CACHE_PORT}"
    else
        terraform apply -lock=false -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}" -var=database_password="${DATABASE_PASSWORD}" -var=database_user="${DATABASE_USER}" -var=database_name="${DATABASE_NAME}" -var=postgres_ip="${POSTGRES_IP}" -var=environment="staging" -var=gs_bucket_name="${GS_BUCKET_NAME}" -var=gs_bucket_url="${GS_BUCKET_URL}" -var=cache_ip="${IP_ADDRESS}" -var=cache_port="${CACHE_PORT}"
    fi
}

main() {
    download_terraform
    prepare_deployment_script
    check_branch
    initialise_terraform
    destroy_previous_infrastructure
    build_current_infrastructure
}

main "$@"
