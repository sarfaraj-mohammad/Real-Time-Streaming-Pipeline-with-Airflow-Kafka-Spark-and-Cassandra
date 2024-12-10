# Real-Time Streaming Pipeline with Airflow, Kafka, Spark, Cassandra, and Docker

This repository contains an end-to-end data engineering project that demonstrates the implementation of a real-time streaming pipeline. The pipeline is orchestrated using Airflow, processes data via Kafka and Spark Structured Streaming, and stores the output in Cassandra, all containerized with Docker.

## Project Overview

The goal of this project is to simulate real-time data streaming by generating random user data, streaming it into Kafka topics, processing it using Spark, and storing the processed data in Cassandra for persistence. The pipeline is managed using Airflow DAGs.

## Components and Files
1.  docker-compose.yaml
- Contains the configuration for all required services, including Airflow, Kafka, Zookeeper, Cassandra, and Spark.
- Run this file to set up the entire infrastructure.

2.  stream_to_kafka.py
- Generates random user data using the Random Name API.
- Publishes the generated user data to a Kafka topic.
- Scheduled to run daily using an Airflow DAG.

3.  airflow_dag.py
- Defines an Airflow DAG to orchestrate the execution of stream_to_kafka.py.
- Configured to run at 1:00 AM daily.

4.  cassandra_setup.cql
- Creates the necessary Cassandra keyspace (social_network) and table (users).
- Run this script to set up the Cassandra schema.

5.  kafka_to_cassandra_using_spark.py
- A PySpark Structured Streaming script to:
  - Read user data from the Kafka topic.
  - Process and write the data to the Cassandra keyspace and table created earlier.
- This script integrates Spark, Kafka, and Cassandra.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Docker and Docker Compose
- Python 3.x

### Steps to Run the Project

1.  Clone the Repository
    ```bash
    git clone https://github.com/sarfaraj-mohammad/Real-Time-Streaming-Pipeline-with-Airflow-Kafka-Spark-and-Cassandra.git
    ```
    ```bash
    cd Real-Time-Streaming-Pipeline-with-Airflow-Kafka-Spark-and-Cassandra
    ```
    
    Initializing the Environment:
    
    Before starting Airflow for the first time, you need to initialize the environment, create necessary files, directories, and set up the database. Run this command only once to initialize the Airflow environment:
    ```bash
    docker compose up airflow-init
    ```
    
    After initialization is complete, you should see a message like this:
    
    airflow-init_1       | Upgrades done \
    airflow-init_1       | Admin user airflow created \
    airflow-init_1       | 2.10.3 \
    start_airflow-init_1 exited with code 0 \
    The account created has the login airflow and the password airflow.
    
    Directories Mounted in the Container:
    - ./dags: Place your DAG files here.
    - ./logs: Contains logs from task execution and scheduler.
    - ./config: You can add custom log parsers or configure cluster policies via airflow_local_settings.py.
    - ./plugins: Put custom plugins here.


2.  Start the Docker Containers (spin up all the services) by running:
    ```bash
    docker-compose up -d
    ```


3.	Access the Airflow UI:
    - Go to Airflow UI at localhost:8080.
    - Check if a DAG named “random_users” is imported successfully.
    - If yes, start the DAG and run it. If there are errors (e.g., import errors), resolve them.


4.	Access the Kafka UI:
    - Go to Kafka UI at localhost:8888.
    - Look for the “random_users” topic and verify if messages are being pushed to this topic.


5.	Setup the Cassandra Keyspace and Tables:
    - Access the Cassandra server’s interactive terminal:
    ```bash
    docker exec -it cassandra /bin/bash
    ```
    
    - Once inside the bash, access the cqlsh CLI:
    ```bash
    cqlsh -u cassandra -p cassandra
    ```
    
    - Run the Cassandra setup script:
    ```bash
    SOURCE '/home/cassandra_setup.cql'
    ```
    
    - Verify that the keyspace and table were created successfully.


6.	Access the Spark CLI:
    ```bash
    docker exec -it spark_master /bin/bash
    ```
    
    - Run the PySpark job:
    ```bash
    spark-submit --master local[2] --packages com.datastax.spark:spark-cassandra-connector_2.12:3.3.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /home/kafka_to_cassandra_using_spark.py
    ```



7.  Verify Data in Cassandra
    - Check if the user data has been successfully written to the Cassandra table:
    ```bash
    docker exec -it <cassandra-container-name> cqlsh -u cassandra -p cassandra
    ```
    ```bash
    SELECT * FROM social_network.users;
    ```


Key Features
- Real-Time Data Streaming: Simulates real-time data flow using Kafka and PySpark Structured Streaming.
- Orchestration with Airflow: Schedules and manages the workflow.
- Data Persistence: Stores processed data in a Cassandra database for efficient querying.
- Containerized Setup: Simplifies deployment and management using Docker.

Future Enhancements
- Extend the pipeline for more complex data transformations in Spark.
- Add monitoring and alerting for failed DAG runs.
- Incorporate a REST API for real-time data access.

## Contributors

Contributions are welcome! If you’d like to extend this project or adapt it for your use case:
1. Fork the repository to create your copy.
2. Work on your enhancements or bug fixes in a feature branch.
3. Submit a Pull Request (PR) with a clear description of your changes.

For any issues, suggestions, or bug reports, feel free to open an issue or reach out directly. Collaboration and feedback are highly appreciated!
