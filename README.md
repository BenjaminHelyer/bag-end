# bag-end
This project is a personal website launched on AWS, complete with a custom CI/CD pipeline.
As such, please excuse the readme for being a bit more personal.

Some time ago, my grandfather asked me, "So what is this cloud that we keep hearing about?"
As an engineer, I was ashamed that I had absolutely no clue how to answer. Thus, the
purpose of this project, is, in some way, an answer to my grandfather's question.

The website uses all the happy cloud resources. What I mean by this: it uses a
serverless resource (Lambda), a NoSQL database (DynamoDB), and a content delivery network (CloudFront). 
The repository has a CI/CD pipeline that uses IaC to deploy the resources.
