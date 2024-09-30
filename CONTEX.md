
  
# Monitoring Python Application with Prometheus



![](https://miro.medium.com/v2/resize:fit:1400/1*SFptFXsyIvaJnfMcPfJcnw.png)

Monitoring Python Application with Prometheus

This article aims to outline the basics of Prometheus and also learn to monitor the Python application using Prometheus and Grafana.

# What are Metrics ?

Metrics are the quantitative measurements used to understand historic trends, correlate diverse factors and measure changes in your performance, consumption, or error rates. They are the raw data be collected from various sources. These sources can be hardware, applications, websites. Average response time, Error rates, Request rate, CPU and memory metrics are the few examples.

# What is Monitoring ?

Monitoring is the process that transforms streams of raw data into useful information . It is the process of collecting, aggregating and analysing data to raise awareness of the characteristics and behaviour of components. It is vital for ensuring the optimal performance, health and reliability of system.

# What is Prometheus?

![](https://miro.medium.com/v2/resize:fit:520/1*-IMhOcXw30-occlA4seERQ.jpeg)

Prometheus

It is a metric monitoring tool that collects and stores its metrics as time series data, i.e. metrics information is stored with the timestamp at which it was recorded, alongside optional key-value pairs called labels.

## Features of Prometheus

1. **_Multi-dimensional data-_** It uses multi-dimensional data model to represent time-series data , hence allowing flexibility in organising and querying metrics based on various dimensions like job, instance and labels, thus enabling the detailed analysis
2. [**_PromQL_**](https://prometheus.io/docs/prometheus/latest/querying/basics/)**_-_** Uses powerful query language to slice and dice collected time series data
3. **_Alerting rules-_** It allows to define rules based on specified conditions. If the system detects that a predefined condition it triggers an alert
4. **_Data visualisation-_** It allows to visualise data through integrations with other tools like Grafana. Grafana is an open-source analytics and monitoring platform that allows users to create visually appealing dashboards and reports based on the data collected by Prometheus.

![](https://miro.medium.com/v2/resize:fit:400/1*ggKqW2DHYS3am6niuaxRiQ.png)

Grafana

# Key Terms in Prometheus

![](https://miro.medium.com/v2/resize:fit:1400/1*h8IDBhJj5cxdCAG_WqtEfQ.png)

Key Terms

# Types of Metrics

![](https://miro.medium.com/v2/resize:fit:1400/1*ctxvdS6iYhVabyAQ_l219g.png)

Types of Metrics

# Metrics Vs Logs

![](https://miro.medium.com/v2/resize:fit:1400/1*uE57WYRWCQKYyWt60WvstQ.png)

Metrics Vs Logs

# Getting Started

We will create a simple project by building an application(PyUniversity) that allows users to search and view the courses/blogs and also integrate the application with Prometheus and Grafana.

![](https://miro.medium.com/v2/resize:fit:1128/1*QaBxw-cgpW5hv7VqDqT57w.png)

PyUniversity Application integrated with Prometheus and Grafana

![](https://miro.medium.com/v2/resize:fit:1400/1*5eeDzZ0ez35jI67zVVQavg.png)

PyUniversity Service API’s

# 1. Setup- Installations and Downloads

- Download the [couchbase](https://www.couchbase.com/downloads/?family=couchbase-server) [server](https://www.couchbase.com/downloads/?family=couchbase-server) [community](https://www.couchbase.com/downloads/?family=couchbase-server) [version](https://www.couchbase.com/downloads/?family=couchbase-server). Post download, create a new cluster with new bucket and user. Give bucket name and username of your choice and use the same names (bucketname , username and password) in [.env](https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1) file
- Download the [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Install [docker compose](https://docs.docker.com/compose/install/)
- Install [couchbase](https://pypi.org/project/couchbase/), [load_dotenv](https://pypi.org/project/python-dotenv/), [flask](https://flask.palletsprojects.com/en/2.1.x/installation/), [flask-restx](https://pypi.org/project/flask-restx/), [prometheus_client](https://pypi.org/project/prometheus-client/) packages

# 2. Project Structure

![](https://miro.medium.com/v2/resize:fit:1104/1*YlpQxkyAThMSzXJwMwiZeA.png)

Project Structure
# 4. Run

- Navigate the path where docker-compose file is present and Run the Docker composition from docker desktop terminal

docker-compose up -d

![](https://miro.medium.com/v2/resize:fit:1400/1*lTLpEHkXnqJCjGgoYpYT2Q.png)

docker-compose command execution

- Open terminal and run the application using below command

python3 app.py

- Open a new terminal and create few courses by executing the below curl
```
curl -H 'Content-Type: application/json' -d '{ "courseName":"Implementing gRPC In Python","courseId":"CR0013", "url" : "https://ashishmj.medium.com/implementing-grpc-in-python-51dd6be87ec3" , "duration": 70 ,"author": "Ashish MJ" ,"description" : "Course aims to outline the basics of gRPC and create a simple project by building endpoints using gRPC"}' -X POST http://localhost:5000/pyacademy/courses  
  
curl -H 'Content-Type: application/json' -d '{ "courseName":"REST APIs in Go using Gorilla Mux","courseId":"CR0012", "url" : "https://blog.devgenius.io/rest-apis-in-go-using-gorilla-mux-01fab932c5a0" , "duration": 30 ,"author": "Ashish MJ" ,"description" : "Course aims to outline the basics of REST architecture and create a simple project by building REST APIs using Gorilla mux"}' -X POST http://localhost:5000/pyacademy/courses  
  
curl -H 'Content-Type: application/json' -d '{ "courseName":"Build Microservices with Python","courseId":"CR0011", "url" : "https://blog.devgenius.io/build-microservices-with-python-63fd35fa3baa" , "duration": 90 ,"author": "Ashish MJ" ,"description" : "Course aims to outline the basics of Microservices based architecture and learn how to build microservices with Python"}' -X POST http://localhost:5000/pyacademy/courses  
  
curl -H 'Content-Type: application/json' -d '{ "courseName":"Implement CI / CD using Jenkins for Python Application","courseId":"CR0010", "url" : "https://blog.devgenius.io/implement-ci-cd-using-jenkins-for-python-application-91a3bcf7d91" , "duration": 45 ,"author": "Ashish MJ" ,"description" : "Course aims to outline the basics of Jenkins and learn how to implement Continuous Integration / Continuous Delivery using Jenkins for a Python application"}' -X POST http://localhost:5000/pyacademy/courses

```
- Open any browser and type [http://localhost:5000/pyuniversity/home](http://localhost:5000/pyuniversity/home). The home page of the PyUniversity will be rendered

![](https://miro.medium.com/v2/resize:fit:1400/1*Z7mZDyVRoyNjxtc88Bo9Wg.png)

Home Page- Pyuniversity

# 5. Sanity Test

- Open any browser and type [http://localhost:9090](http://localhost:9090/). You will navigate to the home page of Prometheus. Then click on target button from Status menu, you will find all the exporters from which Prometheus retrieves metrics

![](https://miro.medium.com/v2/resize:fit:1400/1*_PJUlELolsjHImS7FTYFLg.png)

Prometheus Screen

- Open any browser and type [http://localhost:3000](http://localhost:3000/). You can now access the [Grafana Web UI](http://localhost:3000/) using the default login/password `admin/admin`

![](https://miro.medium.com/v2/resize:fit:1400/1*Wgapf6sFnv2wZvhNbxnqfw.png)

Grafana Screen

- **Search Course-** Enter the course to be searched and click on search button

![](https://miro.medium.com/v2/resize:fit:4248/1*tDT7xBlBa2S9tTz0pRNr-A.png)

![](https://miro.medium.com/v2/resize:fit:5716/1*cuGIJSwhYBzAX9lx6Qjqlw.png)

Searching courses

# 6. Visualization with Grafana

We had defined 2 metrics for our application -

- app_request_count (Counter type metric with _method_, _endpoint_, _http_status_ as metric label)
- app_request_latency_seconds(Histogram type metric with _method_, _endpoint_, _http_status_ as metric label)

In the [Explore view](http://localhost:3000/explore), you can use the following expression `app_request_count_total` to visualise the total successful hits to home page , successful search and unsuccessful search.

![](https://miro.medium.com/v2/resize:fit:1400/1*hAWoTmX_wBljJAQ8ZrxzGA.png)


