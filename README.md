# pyUniversity

```bash
docker-compose up -d -f config/docker-compose.yml
# Open terminal and run the application using below command

python3 app.py

Open a new terminal and create few courses by executing the below curl
curl -H 'Content-Type: application/json' -d '{ "courseName":"Implementing gRPC In Python","courseId":"CR0013", "url" : "https://ashishmj.medium.com/implementing-grpc-in-python-51dd6be87ec3" , "duration": 70 ,"author": "Ashish MJ" ,"description" : "Course aims to outline the basics of gRPC and create a simple project by building endpoints using gRPC"}' -X POST http://localhost:3500/pyuniversity/courses

curl -H 'Content-Type: application/json' -d '{ "courseName":"REST APIs in Go using Gorilla Mux","courseId":"CR0012", "url" : "https://blog.devgenius.io/rest-apis-in-go-using-gorilla-mux-01fab932c5a0" , "duration": 30 ,"author": "Ashish MJ" ,"description" : "Course aims to outline the basics of REST architecture and create a simple project by building REST APIs using Gorilla mux"}' -X POST http://localhost:3500/pyuniversity/courses

curl -H 'Content-Type: application/json' -d '{ "courseName":"Build Microservices with Python","courseId":"CR0011", "url" : "https://blog.devgenius.io/build-microservices-with-python-63fd35fa3baa" , "duration": 90 ,"author": "Ashish MJ" ,"description" : "Course aims to outline the basics of Microservices based architecture and learn how to build microservices with Python"}' -X POST http://localhost:3500/pyuniversity/courses

curl -H 'Content-Type: application/json' -d '{ "courseName":"Implement CI / CD using Jenkins for Python Application","courseId":"CR0010", "url" : "https://blog.devgenius.io/implement-ci-cd-using-jenkins-for-python-application-91a3bcf7d91" , "duration": 45 ,"author": "Ashish MJ" ,"description" : "Course aims to outline the basics of Jenkins and learn how to implement Continuous Integration / Continuous Delivery using Jenkins for a Python application"}' -X POST http://localhost:3500/pyuniversity/courses
#you can access the application at:
Open any browser and type http://localhost:3500/pyuniversity/home. The home page of the PyUniversity will be rendered
```

```bash
#you can access CouchDB admin at:
curl -u $CB_USERNAME:$CB_PASSWORD  http://$CB_HOST/pools

http://localhost:5984/_utils/#login
```

```bash
#Sanity Test
#Open any browser and type 
http://localhost:9090/ 
#You will navigate to the home page of Prometheus. 
# Then click on target button from Status menu, you will find all the exporters from which Prometheus retrieves metrics
```