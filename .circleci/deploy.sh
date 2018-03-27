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
    git clone -b continuous-deployment-156068297 https://github.com/JamesKirkAndSpock/Hirola-Deployment-Script.git
    cd ~/Hirola-Deployment-Script
    mkdir account-folder
    cd account-folder
    touch account.json

    echo ${SERVICE_ACCOUNT} > ~/Hirola-Deployment-Script/account-folder/account.json
}

check_branch(){
    echo "$CIRCLE_USERNAME"
    if [[ "$CIRCLE_USERNAME" == "JamesKirkAndSpock" && "$CIRCLE_BRANCH" != 'develop' && "$CIRCLE_BRANCH" != 'master' ]]; then
        HOST=${DEVOPS_HOST}
        ENVIRONMENT=${DEVOPS_ENVIRONMENT}
        IP_ADDRESS=${DEVOPS_IP_ADDRESS}
    fi

    if [ "$CIRCLE_BRANCH" == 'develop' ]; then
        HOST=${DEVELOP_HOST}
        ENVIRONMENT=${DEVELOP_ENVIRONMENT}
        IP_ADDRESS=${DEVELOP_IP_ADDRESS}
    fi

    if [ "$CIRCLE_BRANCH" == 'master' ]; then
        HOST=${MASTER_HOST}
        ENVIRONMENT=${MASTER_ENVIRONMENT}
        IP_ADDRESS=${MASTER_IP_ADDRESS}
    fi
}

initialise_terraform() {
    cd ~/Hirola-Deployment-Script
    terraform init -backend-config=bucket="${GCP_BUCKET}" -backend-config=prefix="/hirola-terraform/${ENVIRONMENT}/terraform.tfstate"
}

destroy_previous_infrastructure(){
    if [[ "$CIRCLE_USERNAME" == "JamesKirkAndSpock" && "$CIRCLE_BRANCH" != 'develop' && "$CIRCLE_BRANCH" != 'master' ]]; then
        terraform destroy -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}" -var=region="${DEVOPS_REGION}" -var=zone="${DEVOPS_ZONE}"
    else
        terraform destroy -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}"
    fi

}

build_current_infrastructure() {
    if [[ "$CIRCLE_USERNAME" == "JamesKirkAndSpock" && "$CIRCLE_BRANCH" != 'develop' && "$CIRCLE_BRANCH" != 'master' ]]; then
        terraform apply -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}" -var=region="${DEVOPS_REGION}" -var=zone="${DEVOPS_ZONE}"
    else
        terraform apply -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}"
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
