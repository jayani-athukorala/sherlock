# Sherlock - Case File Assistant
This project implements "Sherlock," a detective assistant that will answer questions about case files.


### Prerequisites
- **Docker** and **Docker Compose** installed and running  
  Installation guide: https://docs.docker.com/engine/install/

Verify installation:
```bash
docker --version
```

### Build and Run with Docker Compose

#### From the project root directory, run:

```bash
docker compose up --build
```
This will Build the application image, Database Volume, Start the Sherlock application and required services and Expose the at port 8000 in your hosting machine.

#### Upload Files and ask questions
Files Supported : PDF / TXT
Ask Questions : Ex. "What was Mrs. Hudson's alibi?"

#### Stop and Remove Containers
To stop and clean up all running containers:

```bash
docker compose down
```

### Remove all containers, images, volumes, networks, and build cache
```bash
docker system prune -a --volumes

```

