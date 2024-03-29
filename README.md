# Daily-Grind-Final-Project

Developer's: 
[Rosana ThanaraJan](https://github.com/rosana-t),
[Sumaya Jama](https://github.com/sumayaja),
[Jorge Caneda Gomez](https://github.com/jorgecaneda),
[Mihaly Zoltan Jeles](https://github.com/MihalyJeles)

# About Us

Daily Grind is an app to that utilises a fully scalable ETL (Extract, Transform, Load) pipeline to handle large
volumes of transaction data for Super Cafe. This pipeline will collect all the transaction data generated by each individual café and place it
in a single server. By being able to easily query the company's data as a whole, the client will drastically increase their ability to identify company-wide trends and insights.


# Elevator Pitch

For Super Cafe:
Who - want to target new and existing customers and also understand what products are selling well. They want to access data from different stores and use that data to identify trends within the sales.

The Super cafe website:
Is a  - A website that allows the client to view data to help grow their business.
That - Allows the client to view customer trends and data from different shops.
Unlike - Mini project app where we had no trends or existing data.
Our Product - Will allow client to view trends due to the ETL pipelines. 

# Scope

Time - Limited time to do the project as we only have 5/6 weeks, therefore focus on the key requirements. The availability of the team (1).
Quality - Functional code with unit testing (2).
Budget - Resources given by the instructors during the program (1).
Scope - Must be able to read, transform, upload and transfer data from each branch to a database so the client can increase the product sales and be able to grow their business from viewing the trends (3/4).

# MoSCoW

Must Have -
Basic CLI for client input and output.
Read existing data from the CSV files .
Store, upload and transform data for the CSV files.
AWS Database and build ETL pipelines.
Docker Compose.
Python Code.
Agile.
Git Hub.
Visualise the data using graphs - Grafana.

Should Have - 
Easy to read CLI for the user.
Normalise the data.

Could Have - 
Another website for client interface.
Draw a plan of our project so the team are all on the same page.
Being able to remove sensitive data.
Login for security.
Improve the access to the data for the client(connection between products and branches).

Won't Have - 
Extracted data that we don't need.
Each branch won’t have the transformed data, only management team etc. of the client.

# The approach
![Daily Grind 1](https://user-images.githubusercontent.com/127961119/231802098-93dc852a-dcda-4a7b-9156-9619b74946ad.png)

# SMART goal
Organise our team to work cohesively together and building upon our strengths and helping each other in are weaknesses.

# Ways of working
https://docs.google.com/document/d/19KHkB9tTL4QzMGErdRBYX49L5XkttYZl1tBRzudbow8/edit

# Required libraries and modules

For the app.py:
```ruby
import csv
from datetime import datetime
```

For the connect_rs_database.py:
```ruby
import json
import boto3
import psycopg2
```

For the connection_database.py:
```ruby
import psycopg2
import os
from dotenv import load_dotenv
```

For the lambda_function_to_create_tables:
```ruby
import json
import boto3
import psycopg2
from connection_database import set_up_rs_connection
```

For the lambda_function.py:
```ruby
import boto3
import psycopg2
import csv
import json
from app import *
from connect_rs_create_table import *
```

For the six.py:
```ruby
from __future__ import absolute_import
import functools
import itertools
import operator
import sys
import types
```

For the test_unit.py:
```ruby
from unittest.mock import Mock,patch
import pytest
from app import *
```

# Command line for installations on Windows

-If you are on Mac you will need to use (python3) instead of (py).

## How to set up a Python 3.10 environment for the Final Project (Windows, GitBash):

1.) Download Python 3.10 latest version to your computer and install it.

2.) Setup a new virtual environment in VsCode using GitBash:

- Open the daily-grind-final-project folder in VsCode
		
- Create a virtual environment: 
```ruby
py -3.10 -m venv .venv
```
- Activate it: 		
```ruby
source .venv/Scripts/activate
```


## Creating a branch:
Open a Git Bash terminal in the daily-grind-final-project directory

To create a branch enter:
```ruby
git branch (name the branch on the Trello ticket number) eg. $ git branch 8._Updating_README_file
```

To move into the new branch in your local repository enter:
```ruby
git checkout <name of branch> 
```

To push the branch into the Git repository:
```ruby
git push --set-upstream origin <name of branch> 
```

Add, Commit and Push the branch to the main repository. Check in Github if the branch is on the Git repository. 

## Pull Request: 
When we have finished writing our code and want to merge it, we will carry out a pull request and assign the scrum master to review the code. 

## Merging the branches:
Once the scrum master and the team are happy with the code we will merge the code with:
```ruby
git checkout main (to return to the main branch)
```
```ruby
git pull (on your local repository)
```

## Deleting a Branch: 
The branch will be deleted once the ticket is complete if it has already been fully merged in its upstream branch:
```ruby
git --delete <name of branch> 
```

## PostgreSQL and Docker compose:
To install psycopg2:
```ruby
py -m pip install psycopg2
```

To install python-dotenv:
```ruby
py -m pip install python-dotenv
```

To pull PostgreSQL docker image:
```ruby
docker pull postgres
```

To start the container:
```ruby
docker-compose up -d
```

## AWS:
To login:
```ruby
aws sso login --profile <profile_name>
```

## Unit-Test:
To install pytest:
```ruby
py -m pip install pytest 
```
To run a single test:
```ruby
py -m pytest <name of the test_function> -v
```

To run all the tests:
```ruby
py -m pytest -v
```

## Grafana:

### For all the members in the team to be able to acces Grafana:

1.) One person in the team is going to create a new instance and a new secuirty group in AWS using AWS "Amazon Linux v2" machine image and they will end up with the SSH key.

2.) Save the key into any directory.

3.) Connect into the instance using SSH.

4.) Run the following code:

```ruby
chmod 400 Daily-Grind-Key.pem
```

```ruby
ssh -i "Daily-Grind-Key.pem" ec2-user@ec2-34-244-12-214.eu-west-1.compute.amazonaws.com
```

```ruby
sudo yum install -y amazon-linux-extras
```

```ruby
sudo amazon-linux-extras install docker -y
```

```ruby
sudo service docker start
```

```ruby
sudo usermod -a -G docker ec2-user
```

```ruby
sudo chkconfig docker on
```

```ruby
sudo docker run -d -p 80:3000 grafana/grafana
```

5.) Then acsess Grafana using the Public IPv4 address on the Instance created before.

- Replace (https to http://) on the web adress.

- Log in with the user and password..
