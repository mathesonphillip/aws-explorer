
<!-- Just a file that contains questions for chatgpt -->



- I also want to allows for posibly creating a command line interface (CLI) to help manage, query and report on AWS resources.
  - I will use the `click` package to create the CLI.
  - I will use the `tabulate` package to create the CLI output.
  - I will use the `aws-explorer` package to create the CLI commands.

---

- I need help trying to understand how to breakup my package.
- I've been told its best practice to keep logging/output separate from the business logic.
  - I'm not sure how to do this.
  - I'm not sure how to test this.

---

How to do testing


---


How to do package management


---

I needed to create a SessionManager class which uses the `configparser` package to read the `config.ini` file and create a boto3 session. What would be the best way to do this?
I require the ability to create multiple boto3 sessions, if required. This will all leverage AWS Named profiles.

----

I really like how the SessionManager is setup. However, how would i have the SessionManager interact with the other classes? I want to be able to create a boto3 session in the SessionManager class and then pass that session to the other classes, such as the EC2Managaer. I'm not sure how to do this.



----

Suppose the session manager class contains all the aws service boto3.clients and boto3.resource objects.
How would i pass these objects to the other classes? I want to be able to create a boto3 session in the SessionManager class and then pass that session to the other classes, such as the EC2Managaer. Does this sound reasonable?
Or should the EC2Manager class create its own boto3.resource and boto3.client objects? The challenge is that i want to be able to create multiple boto3 sessions, if required.
I think the logic to interact with EC2 be within the EC2Manager class, im just not sure if the client/resource should be there also 



----


What is i had an Account class which encapsulated the SessionManager class and the EC2Manager class? 
Fundamentally, the Account does kind of own these.
This would allow me to create a list of Account objects, which would contain the SessionManager and other service classes.



Would this be a good idea? I'm not sure how to do this. I want to be able to create a boto3 session in the SessionManager class and then pass that session to the other classes, such as the EC2Managaer. I'm not sure how to do this.


* Write an example 
* Write an example SessionManager class which uses the 