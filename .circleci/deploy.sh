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
    if [ "$CIRCLE_USERNAME" == "JamesKirkAndSpock" ]; then
        git clone -b continuous-deployment-156068297 https://github.com/JamesKirkAndSpock/Hirola-Deployment-Script.git
    else
        git clone -b non-telegram-continuous-deployment-156068297 https://github.com/JamesKirkAndSpock/Hirola-Deployment-Script.git
    fi
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
        REGION=${DEVOPS_REGION}
        ZONE=${DEVOPS_ZONE}
    fi

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
    terraform init -backend-config=bucket="${GCP_BUCKET}" -backend-config=prefix="/hirola-terraform/${ENVIRONMENT}/terraform.tfstate"
}

destroy_previous_infrastructure(){
    if [[ "$CIRCLE_USERNAME" == "JamesKirkAndSpock" || "$CIRCLE_BRANCH" == 'develop' || "$CIRCLE_BRANCH" == 'master' ]]; then
        terraform destroy -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}" -var=region="${REGION}" -var=zone="${ZONE}"
    else
        terraform destroy -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}"
    fi

}

build_current_infrastructure() {
    if [[ "$CIRCLE_USERNAME" == "JamesKirkAndSpock" || "$CIRCLE_BRANCH" == 'develop' || "$CIRCLE_BRANCH" == 'master' ]]; then
        terraform apply -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}" -var=region="${REGION}" -var=zone="${ZONE}"
    else
        terraform apply -auto-approve -var=project="${PROJECT_ID}" -var=ip-address="${IP_ADDRESS}" -var=env="${ENVIRONMENT}" -var=branch="${CIRCLE_BRANCH}" -var=host="${HOST}"
    fi
}

send_sticker() {
    STICKERS=( "CAADAgADswIAAkb7rASMLYKaSCtm6AI" "CAADAgAD7AYAAnlc4gmyzyRQT6BJSwI" "CAADAgADdAIAArnzlwuPQ69bvLwTLQI" "CAADAgADKQcAAmMr4gnhM9ccDb2hKAI" "CAADAgADHAgAAgi3GQKRQRBYukJHPQI" "CAADAgADnAMAAkKvaQABPPcu6tryHCAC" "CAADAgAD8QADHdMcCujnc2NYpF9LAg" "CAADBAADTwEAAriGNgch8jFBHEA_9gI" "CAADAgADZxIAAkKvaQABvhbl68BnTKUC" "CAADAgAD8gIAAmvEygq7pRRA8OnbFAI" )
    RANDOM=$$$(date +%s)
    STICKER=${STICKERS[$RANDOM % ${#STICKERS[@]} ]}
    curl -s -X POST https://api.telegram.org/bot${TELEGRAM_API_KEY}/sendSticker \
    -d chat_id=${TELEGRAM_CHAT_ID} \
    -d sticker=$STICKER
}

send_message() {
    curl -s -X POST https://api.telegram.org/bot${TELEGRAM_API_KEY}/sendMessage \
    -d chat_id=${TELEGRAM_CHAT_ID} \
    -d text="Your branch "${CIRCLE_BRANCH}" has been deployed. Open http://${HOST} to view it."
}

main() {
    download_terraform
    prepare_deployment_script
    check_branch
    initialise_terraform
    destroy_previous_infrastructure
    build_current_infrastructure
    send_sticker
    send_message
}

main "$@"
