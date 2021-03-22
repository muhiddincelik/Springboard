# STREAMING PROJECT: LOCAL VERSION

### **Building A Local Streaming Pipeline On MacOS**

![bar](./assets/images/bar.jpg)



## Introduction

>  In this project, we will create a local streaming pipeline backed by **Apache Kafka**, **Apache Spark and ELK Stack** using a **Python** client. 
>
>  What we'll build is a log generator and processor. We will generate a stream of logs and then we will write a PySpark script to process those stream of logs to categorize logs: goods, bad and suspicious. We will use data completeness together with consistency with a dimensional user table in MySql as our criteria. Let's look into our design:
>
>  ![bar](./assets/images/design.jpeg)

* Fields of a log:

  

* Our log generator will send the logs to server-logs topic in Kafka.

* Spark Structued Streaming will read these messages in realtime and will split the micro batches into 3 categories:

  - **bad_logs**: If logs are not following our desired data type schema or if they embed a null value in any field. 
  - **suspicious_logs**: We compare log's device type against the user's default device type in our **users** table in MySQL dim_users database. If they don't match we label the log as suspicious. We do this by joining micro batch with **users** dimensional table on **account_id** and **device** fields.
  - **good_logs:** If a log is not bad or suspicious, we label it as 'good'.



## PART A: Infrastructure

### 1) Requirements

* Install Java 8

* We need to install Kafka, Spark (3.1), MySQL and ELK stack. We can utilize home brew to install required services on Mac OS. 

  ```basic
  brew install kafka
  brew install elasticsearch
  brew install logstash
  brew install kibana
  ```

* Install MySQL
* We need modules in [requirements.txt](./generator/requirements.txt) installed for our python execution environment.

### 2) Configurations

+ For Kafka we need to configure server.properties.

  ```
  # Uncomment listener setting as:
  listeners=PLAINTEXT://localhost:9092
  ```

- For MySQL, I configured settings below. Feel free to change.
  - **Port**: 3306
  - **Username**: root
  - **Password**: root1234

* Don't forget to export KAFKA_HOME and SPARK_HOME path. I have added lines below to the ~/.bash_profile for zsh.

  ```
  export SPARK_HOME=/<local path to spark bin folder>/
  export KAFKA_HOME=/<local path to spark bin folder>/
  export PATH=$PATH:$KAFKA_HOME/bin
  export PATH=$PATH:$SPARK_HOME/bin
  ```

  

* We need to locate and edit **logstash_sample.conf** file in logstash config folder.  We can change the name of the conf file.

  ```yaml
  # logstash.conf
  # We read from a Kafka topic as input
  input {
      kafka {
              bootstrap_servers => "localhost:9092"
              topics => ["server-logs-status"]
      }
  }
  
  # We parse the original json message into fields, then filter out the original message
  filter {
        json {
          source => "message"
        }
  
        mutate {
          remove_field => [ "message" ]
        }
  
      }
  
  # We send the data to the 'server-logs' index in elastichsearch from where Kibana will read
  output {
     elasticsearch {
        hosts => ["localhost:9200"]
        index => "server-logs"
        workers => 1
      }
  }
  
  ```

  

### PART B: Execution ###

### 1) Running The Pipeline

Firstly we need to source our bash profile to export paths:

```
source ~/.bash_profile
```

Now we can get our pipeline going by running run the starter bash file ([run.sh](run.sh)). This bash file will start log generator and then immediately submit our processing PySpark script ([processor](./spark_processor.py)).

```bash
# After navigating to the project main folder:
bash run.sh
```



### 2) Verify the results

- Firstly we need to check we have the topics created, if everything is okay, we are supposed to see **server-logs** and **server-logs-status** topics. If we see server-logs-status is in the topic list, it means our spark script works.

```bash
kafka-topics --list --zookeeper zookeeper:2181
```

* Then we can read messages in the console:

  ```bash
  kafka-console-consumer --bootstrap-server broker:9092 --topic server-logs --from-beginning
  kafka-console-consumer --bootstrap-server broker:9092 --topic server-logs-status --from-beginning
  ```

* We can check MySQL whether logs are being written into their respective tables.

* Now we can check Kibana (at port 5601) for new data, if it notifies that there is new data, then we create index pattern for our logs. Then we can build a simple realtime dashboard for log counts per category:

  ![](./assets/images/kibana.png)

