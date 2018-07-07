AWS CERTIFICATION PREP
======================

Project Status
--------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Project Start
     - Jun 4, 2018
   * - Latest Update
     - Jul 7, 2018

`Change Log <https://github.com/addr2data/aws-certification-prep/blob/master/changelog.rst>`_

Introduction
------------
Recently, I decided to pursue AWS certification. Mostly for career reasons, but also because the concept of **Infrastructure as Code** fascinates me. I've been playing with AWS EC2, off and on, since 2012, but have never used it in a meaningful way. Considering how much the AWS ecosystem has grown over the years, it seems, I have my work cut out for me.

In addition to certification, I want to become a highly skilled user of AWS services. I have a small, but reasonable budget for AWS spend each month. Combine that with the 'free tier eligibility' of the new account I created for this project and I should be able to get a decent amount of hands-on experience. My goal is to work primarily with the AWS CLI, but I also want to get comfortable writing Python scripts that leverage the API directly, so Boto3 (the AWS Python SDK) will be a necessity.

I have created this public GitHub project to force myself to be more organized and methodical in my approach. I am building out this project as a training resource for others. I know this approach will help me greatly, but I sincerely hope others will find value in it.

**I expect this project to be a work-in-progress for at least 12 months.**

Certifications
--------------
My intention is to pursue the following certifications. I chose the two levels of **Solution Architect** certification, because I felt these would provide, from a career perspective, the most bang for my buck. I added the **Advanced Networking** certification, because I have a strong interest in networking. It is possible these choices will change over time, but for now, this is the plan.  

-  AWS Certified Solutions Architect – Associate
-  AWS Certified Advanced Networking – Specialty
-  AWS Certified Solutions Architect - Professional

Exam Guides
-----------
Here are the links for each of the exam guides/blueprints.

- `AWS Certified Solutions Architect – Associate <https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS_Certified_Solutions_Architect_Associate_Feb_2018_%20Exam_Guide_v1.5.2.pdf>`_
-  `AWS Certified Advanced Networking – Specialty <https://d1.awsstatic.com/training-and-certification/docs-advnetworking-spec/AWS%20Certified%20Advanced%20Networking_Speciality_Exam_Guide_v1.1_FINAL.pdf>`_
-  `AWS Certified Solutions Architect - Professional <https://d0.awsstatic.com/Train%20&%20Cert/docs/AWS_certified_solutions_architect_professional_blueprint.pdf>`_

AWS Services
------------
The following table is provided to show two things:

	- Which AWS services are currently in scope for the project.
	- At what level, a particular AWS service, has been incorporated into the exercises provided below.

Expect this table to change frequently, as new exercises are added.

**Last updated: 6/23/18**

.. list-table::
   :widths: 20, 20, 20, 20, 20
   :header-rows: 0

   * - **Category**
     - **Service**
     - **Basic**
     - **Intermediate**
     - **Advanced**
   * - Compute
     - EC2, ECS, Lambda
     - EC2
     - 
     - 
   * - Storage
     - S3, EFS, Glacier
     - 
     - 
     - 
   * - Database
     - RDS, DynamoDB
     - 
     - 
     - 
   * - Networking & Content Delivery
     - VPC, Route 53, CloudFront
     - VPC
     - VPC
     - 
   * - Management Tools
     - CloudWatch, AWS Auto Scaling, CloudFormation, CloudTrail, Systems Manager
     - CloudFormation, Systems Manager
     - 
     - 
   * - Security, Identity & Compliance
     - IAM
     - IAM
     - 
     - 

Tools
-----
Initially, I will be working with the following 'tools'. I will update this list as I start to work with others.

- AWS Console (I will use this where appropriate)
- AWS CLI
- Python3
- Boto3

Approach
--------
As I develop my knowledge and prepare for the exams listed above, I will be using the following process (for multiple services in parallel).

1. Learn the basics of a service.
2. Get comfortable with the basic configuration and use of that service.
3. Build some basic exercises that others could follow and in the process solidify my own understanding.
4. Dig deeper into that service. Get comfortable with advanced configuration, use and design considerations.
5. Build some advanced exercises that others could follow and in the process solidify my own understanding.
6. Understand how that service fits into an overall architecture.
7. Be able to discuss that service with others, in a sales/services context.
8. Rinse and repeat.

Regarding the exercises in this project
---------------------------------------
Following the exercises in this project will generate costs to your AWS account. These should be relatively small, especially if you are new to AWS (increased eligibility for free-tier). An explanation of the expected costs will be provided at the beginning of each exercise.

Account Setup
-------------
If you follow along with this project. You will need to set up some accounts. Here are the links.

-  `Sign up for AWS account <https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/>`_
-  `Sign up for certification account <https://aws.amazon.com/certification/certification-prep/>`_
-  `Sign up training account <https://www.aws.training/Training/>`_

Prepare
-------
You should familiarize yourself with the following whitepapers before you start.

-  `Overview of Amazon Web Services <https://docs.aws.amazon.com/aws-technical-content/latest/aws-overview/aws-overview.pdf>`_
-  `How AWS Pricing Works <https://d1.awsstatic.com/whitepapers/aws_pricing_overview.pdf>`_
-  `AWS Global Infrastructure <https://aws.amazon.com/about-aws/global-infrastructure/>`_


Exercises
---------
First, I would like to thank 
`Brian Ragazzi <https://github.com/BrianRagazzi>`_ 
for assisting with the exercises in this project.

  - I will be creating exercises that primarily use the CLI.
  - Brian will be creating exercises that primarily use the Management Console.
  - Brian will also be re-creating some of my exercises using the Management Console.

The tables below list the exercises that have been created (or planned) and their format(s). For exercises with both formats, the end result of each is the same.  

  - **CLI** - Primarily uses the **awscli** for configuration.
  - **GUI** - Primarily used the **AWS Management Console** for configuration.

In addition, exercises are divided into two categories:

  - **Foundational**: The goal of these exercises is to build a foundational understanding of a service. They will focus on the configuration one or more components of a single service. Other services may be introduced and/or utilized during these exercises, but will not be the focus.

  - **Functional**: The goal of these exercises is to build functional understanding of multiple services working together. They will focus on the configuration of two or more services to achieve a higher level of functionality.


**We hope you enjoy using these exercises, as much as we enjoyed building them.**

Foundational
~~~~~~~~~~~~

.. list-table::
   :widths: 25, 25, 25, 25
   :header-rows: 0

   * - ex-001
     - Getting started
     - `CLI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-001_GettingStarted.rst>`_
     - 
   * - ex-002
     - Basic VPC configuration
     - `CLI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-002_BasicVpcConfig.rst>`_
     - `GUI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-002_BasicVpcConfigGui.rst>`_
   * - ex-003
     - Testing basic VPC connectivity
     - `CLI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-003_TestingBasicConnectivity.rst>`_
     - `GUI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-003_TestingBasicConnectivityGui.rst>`_
   * - ex-004
     - Getting started with CloudFormation
     - `CLI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-004_GettingStartedCloudFormation.rst>`_
     - 
   * - ex-005
     - Expanding the VPC configuration
     - `CLI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-005_ExpandingVpcConfig.rst>`_
     - 
   * - ex-006
     - Getting started with Load-balancing
     - `CLI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-006_GettingStartedLoadBalancing.rst>`_
     - 
   * - ex-007
     - Working with EBS 
     - `CLI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-007_WorkingEbs.rst>`_
     - 
   * - ex-008
     - Getting started with Snapshots 
     - `CLI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-008_GettingStartedSnapshots.rst>`_
     - 
   * - ex-009
     - Getting started with S3
     - `CLI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-009_GettingStartedS3.rst>`_
     - 
   * - ex-010
     - Getting started with RDS
     - `CLI <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-010_GettingStartedRds.rst>`_
     - 

Functional
~~~~~~~~~~

**Basic Web Server in AWS ecosystem**

.. list-table::
   :widths: 25, 25, 25, 25
   :header-rows: 0

   * - ex-051
     - Basic Web Server in AWS ecosystem (part 1).
     - TBA
     - 
   * - ex-052
     - Basic Web Server in AWS ecosystem (part 2).
     - TBA
     - 
   * - ex-053
     - Basic Web Server in AWS ecosystem (part 3).
     - TBA
     - 
   * - ex-054
     - Basic Web Server in AWS ecosystem (part 4).
     - TBA
     - 
   * - ex-055
     - Basic Web Server in AWS ecosystem (part 4).
     - TBA
     - 


Additional Resources
--------------------

Whitepapers
~~~~~~~~~~~
-  `An Overview of the AWS Cloud Adoption Framework <https://d1.awsstatic.com/whitepapers/aws_cloud_adoption_framework.pdf>`_
-  `AWS Well-Architected Framework <https://d1.awsstatic.com/whitepapers/architecture/AWS_Well-Architected_Framework.pdf>`_
-  `AWS Storage Services Overview <https://d1.awsstatic.com/whitepapers/Storage/AWS%20Storage%20Services%20Whitepaper-v9.pdf>`_
-  `AWS Security Best Practices <https://d1.awsstatic.com/whitepapers/Security/AWS_Security_Best_Practices.pdf>`_
-  `Architecting for the Cloud: AWS Best Practices <https://d1.awsstatic.com/whitepapers/AWS_Cloud_Best_Practices.pdf>`_
-  `The Business Value of AWS: Succeeding at Twenty-First Century Business Infrastructure <https://d1.awsstatic.com/whitepapers/aws-whitepaper-business-value-of-aws.pdf>`_

Videos
~~~~~~
-  `AWS re:Invent 2017: Advanced VPC Design and New Capabilities for Amazon VPC (NET305) <https://www.youtube.com/watch?v=Pj11NFXDbLY>`_

Important Links
---------------
-  `AWS Certification Page <https://aws.amazon.com/certification/certification-prep/>`_
-  `AWS Documentation Page <https://aws.amazon.com/documentation/>`_
-  `AWS Whitepapers Page <https://aws.amazon.com/whitepapers/>`_
-  `AWS Pricing Page <https://aws.amazon.com/pricing/>`_


