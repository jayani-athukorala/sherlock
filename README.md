# Sherlock - Case File Assistant
This project implements "Sherlock," a detective assistant that will answer questions about case files.


## Prerequisites

- **Docker Engine** installed and running.
Can be installed from : https://docs.docker.com/engine/install/

Verify installation:
```bash
docker --version
```

### Build and Run Docker

#### Build the Docker image

```bash
docker build -t sherlock .
```

#### Run the container
```bash
docker run -p 8000:8000 sherlock
```

### Stop and remove the container
```bash
docker rm -f sherlock
```
