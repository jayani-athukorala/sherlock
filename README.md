# Sherlock - Case File Assistant
This project implements "Sherlock," is a containerized RAG-based detective assistant designed to answer questions from uploaded case files. 
It supports document ingestion and intelligent question answering using modern language models.


<<<<<<< HEAD
### Prerequisites
- **Docker** and **Docker Compose** installed and running  
  Installation guide: https://docs.docker.com/engine/install/
=======
## Setting Up the Environment

### Clone the Repository
>>>>>>> f746d84 (Sherlock evaluation)

```sh
git clone https://github.com/jayani-athukorala/sherlock.git
cd sherlock
```

### Install **Docker Engine** 
Docker is required to run the application.
- Installation guide : https://docs.docker.com/engine/install/

- Verify the installation:
```bash
docker --version
```

<<<<<<< HEAD
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

=======
### Environmwnt configuration
- In the project root directory, create a file named ```bash .env```

- Add the provided access token
```bash HUGGINGFACEHUB_API_TOKEN=hf_replace_with_the_token_here
```

## Run the Application

### Build and Start with thr Docker Compose

#### From the project root directory, run:

```bash
docker compose up --build
```
This will :
- Build the application images
- Create and mount the database volume
- Start the Sherlock application and required services
- Expose the API at: http://0.0.0.0:8000

#### Upload documents
Supported file formats: PDF, TXT

#### Ask questions
Example questions:
- “What was Mrs. Hudson’s alibi?”
- “Who was seen leaving the manor at midnight?”

## Stop the applcation

#### Stop and remove containers
To stop and clean up all running containers:

```bash
docker compose down
```

#### Remove all containers, images, volumes, networks, and build cache
```bash
docker system prune -a --volumes

```

>>>>>>> f746d84 (Sherlock evaluation)
