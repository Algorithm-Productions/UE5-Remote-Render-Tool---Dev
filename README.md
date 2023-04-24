# Unreal Engine Remote Render Tool

## Settings / Environment 

Settings found in `.env` file. 

Specify a custom env file with `python app.py --env .local.env` 

## Manager

- Run with: ```python app.py --mode manager```
- Or as docker container (see below)

## Worker

- Run with: ```python app.py --mode worker```
- Or as docker container (see below)

## Submitter

- Run with: ```python app.py --mode submitter```
- Or as docker container (see below)


# Documentation

Todo.

# Docker 

### docker-compose 
docker compose will build the images, create a persistant docker volume and run the container.  
- ```docker compose up --build```

### Building image:
- Navigate to project root directory
- ```docker build -t render_tool .```

### Running Container:
- ```docker run --name render_tool -dp 5000:5000 render_tool```

### Viewing logs:
- ```docker logs -f render_tool ``` # -f to follow logs, leave out to just print to console


# Testing 

```pip install -r test-requirements.txt```
```pytest tests```

