#!/bin/bash
# This shell script deploys a new version to a server.

PROJ_DIR=SWEtastic-journal
VENV=myvirtualenv
PA_DOMAIN="swetasticfour.pythonanywhere.com"
PA_USER='swetasticfour'
DEMO_PA_PWD='swe2024to25'
echo "Project dir = $PROJ_DIR"
echo "PA domain = $PA_DOMAIN"
echo "Virtual env = $VENV"

if [ -z "$DEMO_PA_PWD" ]
then
    echo "The PythonAnywhere password var must be set in the env, export CLOUD_PW=###"
    exit 1
fi


echo "SSHing to PythonAnywhere."
sshpass -p $DEMO_PA_PWD ssh -o "StrictHostKeyChecking no" $PA_USER@ssh.pythonanywhere.com << EOF
    cd ~/$PROJ_DIR; PA_USER=$PA_USER PROJ_DIR=~/$PROJ_DIR VENV=$VENV PA_DOMAIN=$PA_DOMAIN ./rebuild.sh
EOF
