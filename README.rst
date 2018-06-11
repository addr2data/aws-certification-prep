AWS CERTIFICATION PREP
======================

Project Status
--------------		
- Start: 		Jun 4, 2018
- Last Update:	Jun 11, 2018


Introduction
------------
I started playing with EC2 about 6 years ago. I primarily used it to create VMs for dev work. I learned the basics of EC2, never dug in very deeply. A while back, I changed to using Digital Ocean for creating my VMs. Mostly, because of cost differences (at the time) and the simple REST API. Recently, I decided I wanted to come back to using AWS and pursue certification (for career reasons). I have created this GitHub project to help organize my notes/code samples and hopefully, help someone else interested in pursuing AWS certification. I expect it to be a work in progress for 12-18 months.

Exams I have decided to prepare for:
------------------------------------
-  AWS Certified Solutions Architect – Associate
-  AWS Certified Advanced Networking – Specialty
-  AWS Certified Solutions Architect - Professional

Exam Guides
-----------
- `AWS Certified Solutions Architect – Associate <https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS_Certified_Solutions_Architect_Associate_Feb_2018_%20Exam_Guide_v1.5.2.pdf>`_

-  `AWS Certified Advanced Networking – Specialty <https://d1.awsstatic.com/training-and-certification/docs-advnetworking-spec/AWS%20Certified%20Advanced%20Networking_Speciality_Exam_Guide_v1.1_FINAL.pdf>`_

-  `AWS Certified Solutions Architect - Professional <https://d0.awsstatic.com/Train%20&%20Cert/docs/AWS_certified_solutions_architect_professional_blueprint.pdf>`_


Videos you should watch
-----------------------

Networking
----------
-  `AWS re:Invent 2017: Advanced VPC Design and New Capabilities for Amazon VPC (NET305) <https://www.youtube.com/watch?v=Pj11NFXDbLY>`_

Getting started
---------------

Create an AWS account
~~~~~~~~~~~~~~~~~~~~~

Create a certifcation account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a training account
~~~~~~~~~~~~~~~~~~~~~~~~~
https://www.aws.training/Training





Documentation
-------------
https://aws.amazon.com/documentation/
https://aws.amazon.com/certification/certification-prep/
https://aws.amazon.com/whitepapers/

Enterprise Architecture
-----------------------
https://www.zachman.com/about-the-zachman-framework
http://pubs.opengroup.org/architecture/togaf9-doc/arch/index.html



Quizzes
~~~~~~~
https://www.quiz-maker.com/


boto3
-----

Credentials
~~~~~~~~~~~
mkdir ~/.aws
vi ~/.aws/credentials

	[default]
	aws_access_key_id = YOUR_ACCESS_KEY
	aws_secret_access_key = YOUR_SECRET_KEY

Configuration
~~~~~~~~~~~~~
vi ~/.aws/config

	[default]
	region=us-east-1


