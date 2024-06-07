
# Data Processing Pipeline with Airflow and Delta Lake

This repository contains a Docker setup for running a data processing pipeline using Apache Airflow, Spark, and Delta Lake. The pipeline processes data directly from Google Drive, performs transformations, and saves the data in Delta format.

## Pre requisites

Before you begin, ensure you have Docker and Docker Compose installed on your system. You can download them from:
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup and Running

Follow these steps to set up and run the data processing pipeline:

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

### 2. Navigate to the Docker Directory

Change into the Docker directory within the cloned repository:

```bash
cd docker
```
### 3. Start the Docker Compose

Run the following command to start all the services defined in the `docker-compose.yml` file:

```bash
docker-compose up
 ```

This command will build and start all the necessary containers, including Apache Airflow, Spark, and PostgreSQL for Airflow metadata.

### 4. Access Airflow Web Interface

Once the containers are running, open a web browser and access the Airflow web interface at:

```
http://localhost:8082
```

### 5. Log into Airflow

Use the following credentials to log into Airflow:
- **Username:** admin
- **Password:** admin

### 6. Trigger the Pipeline

Navigate to the DAGs tab, find the `pipeline_dag`, and click on the play button to trigger the DAG. This pipeline will:

- Download a CSV file from Google Drive.
- Perform data transformations.
- Save the transformed data in Delta format.

### 7. Check the Output

The transformed data will be saved in the `output` directory inside a Docker volume, which will be created during the setup. You can access this data from your Docker host.

### 8. Using the Data

The saved Delta files can be used as a source for further processing or analysis directly from the `output` directory.

- The source table transformed : output/etl_output
- Average Risk Score Table: output/average_risk_score_table
- Top Sales Table: output/top_sales_table

## Clean Up

To stop and remove the containers, use the following command:

```bash
docker-compose down
```
