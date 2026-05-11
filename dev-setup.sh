#!bin/bash

declare branch='main'
git pull origin $branch

services=("arxiv-crawler" "backend" "frontend")


function check_docker() {
    if ! command -v docker &> /dev/null
    then
        echo "Docker could not be found. Please install Docker and try again."
        exit
    fi
}

function run_service() {
    local service=$1
    echo "Running $service..."
    docker compose -f ../compose-base.yml -f compose.yml up -d --build
}

check_docker

for service in "${services[@]}"
do
    if [ -d "$service" ]; then
        echo "Processing $service"
        cd $service
        cp .env.example .env
        export BASE_DIR=$(pwd)
        run_service $service
        cd ..
    fi
done
