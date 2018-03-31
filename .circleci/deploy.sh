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

initialise_terraform() {
    cd ~/Hirola-Deployment-Script
    terraform init -backend-config=bucket="${GCP_BUCKET}" -backend-config=prefix="/hirola-terraform/${ENVIRONMENT}/terraform.tfstate"
}

destroy_previous_infrastructure(){
    terraform destroy -lock=false -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}"

}

build_current_infrastructure() {
    terraform apply -lock=false -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}"
}

main() {
    download_terraform
    prepare_deployment_script
    initialise_terraform
    destroy_previous_infrastructure
    build_current_infrastructure
}

main "$@"
