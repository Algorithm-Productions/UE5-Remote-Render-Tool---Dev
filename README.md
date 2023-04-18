# Remote Render Tool

Unreal Engine Remote Render Tool


## Docker 

### Building image:
- Navigate to project root directory
- ```docker build -t render_tool .```

### Running Container:
- ```docker run --name render_tool -dp 5000:5000 render_tool```

### Viewing logs:
- ```docker logs -f render_tool ``` # -f to follow logs, leave out to just print to console

