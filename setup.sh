#!bin/bash

declare branch='main'
git pull origin $branch

for dir in ./*
do
    if [ -d "$dir" ]; then
        echo "Processing $dir"
        cd $dir
        cp .env.example .env
        cd ..
    fi
done

echo "================================"
echo "Docker processing... Current directory: $(pwd)"

docker compose -f ./compose-base.yml -f ./arxiv-crawler/compose.yml -f ./backend/compose.yml -f ./front-end/compose.yml down

docker compose -f ./compose-base.yml -f ./arxiv-crawler/compose.yml -f ./backend/compose.yml -f ./front-end/compose.yml up -d --build
