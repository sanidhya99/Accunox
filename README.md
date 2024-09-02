# ACCUNOX

## Project Configuration
Install required dependencies by running the following commands:
    
    apt install docker -y
    apt install docker-compose -y

## Project Setup

Initialize the project successfully with commands:

    docker-compose build --no-cache
    docker-compose up -d

### Precaution 
Before running installation steps ensure Port 5432 and 8000 of your system is not bind to any service already if yes free them up, you can check their availability with command

    sudo lsof -i:5432
    sudo lsof -i:8000