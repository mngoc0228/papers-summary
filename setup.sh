#!bin/bash

declare branch='main'

for dir in ./*                                                
do                                                                                 
    cd $dir
    git pull origin $branch
    cp .env.example .env
    cd ..
fi                                                                
done

docker compose -f ./cmp-base.yml \\
        ./arxiv-crawler/docker-compose.yml \\
        ./backend/docker-compose.yml \\
        ./front-end/docker-compose.yml down

docker compose -f ./cmp-base.yml \\
        ./arxiv-crawler/docker-compose.yml \\
        ./backend/docker-compose.yml \\
        ./front-end/docker-compose.yml up -d --build
