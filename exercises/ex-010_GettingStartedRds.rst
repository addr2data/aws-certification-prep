ex-010: Getting Started with RDS 
================================

Status
------
Draft

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - to be added or none
   * - Prerequisite for exercise(s)
     - to be added or none

Objectives
----------
- To be added

Expected Costs
--------------
The activities in this exercise may result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 0

   * - **Component**
     - **Applicable Costs**
     - **Notes**
   * - To be added
     - 
        + To be added
     -
        + To be added

Limits
------
The following table shows the default limits for the components utilized in this exercise.

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - To be added
     - To be added

Environment variables
---------------------
During these exercises, we will be using the output of some commands to create environment variables. This will help simplify the syntax subsequent commands.

In some places, we will do this manually, because we want to show the the full output of the command. In other places, we will use the **'--query'** and **'--output'** options available in the awscli command to filter the output directly into a variable.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.


Create Stack
------------
Use the following awscli command to create a new CloudFormation **'Stack'** based on the template.

Note: If you are using the **'acpkey1'** Key Pair, you can leave off the **'--parameters'** option all together.

.. code-block::

    aws cloudformation create-stack \
        --stack-name ex-010 \
        --template-body file://templates/ex-010_template.yaml \
        --parameters ParameterKey=KeyPairName,ParameterValue=acpkey1

Output:

.. code-block::

    {
        "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-010/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }

Check the status
----------------
Use the following awscli command to check the **'StackStatus'**.

Rerun this command until **'StackStatus'** is **'CREATE_COMPLETE'**.

.. code-block::

    aws cloudformation describe-stacks --stack-name ex-010

Output:

.. code-block::

    {
        "Stacks": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-010/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "StackName": "ex-010",
                "Parameters": [
                    {
                        "ParameterKey": "KeyPairName",
                        "ParameterValue": "acpkey1"
                    }
                ],
                "CreationTime": "2018-07-04T13:53:02.143Z",
                "RollbackConfiguration": {},
                "StackStatus": "CREATE_IN_PROGRESS",
                "DisableRollback": false,
                "NotificationARNs": [],
                "Tags": [],
                "EnableTerminationProtection": false
            }
        ]
    }

Review the Stack details
------------------------
Use the following awscli command to display the **'LogicalResourceId'** and **'PhysicalResourceId'** for all the components in the **Stack**

Notice the format of this portion of the query string **'{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'**, it adds a header to each column.** 

.. code-block::

    aws cloudformation describe-stack-resources \
        --stack-name ex-010 \
        --output table \
        --query 'StackResources[*].{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'

Output:

.. code-block::

    -------------------------------------------------------------
    |                  DescribeStackResources                   |
    +----------------------------+------------------------------+
    |     Logical Resource Id    |    Physical Resource Id      |
    +----------------------------+------------------------------+
    |  AssociateSubnetRouteTable |  rtbassoc-0dc28d50b1af161b8  |
    |  AttachInternetGateway     |  ex-01-Attac-14DL9YNLFF55U   |
    |  DefaultRoute              |  ex-01-Defau-12BB45W1SQYTD   |
    |  InternetGateway           |  igw-0e52da8418ddc2f40       |
    |  PublicInstance            |  i-05df700205b9a1dc5         |
    |  RouteTable                |  rtb-06240bbb409d1c520       |
    |  SecurityGroupInstance     |  sg-0f8c305fe65cc87bc        |
    |  SecurityGroupRds          |  sg-0582c7bc25a2f5829        |
    |  SubnetPrivate1            |  subnet-09b426c07ac3f155a    |
    |  SubnetPrivate2            |  subnet-006ab0717bdb18170    |
    |  SubnetPublic              |  subnet-06e4ec2717f9d5a7b    |
    |  VPC                       |  vpc-0850e7f16ce7f1b5a       |
    +----------------------------+------------------------------+

Environment variables
~~~~~~~~~~~~~~~~~~~~~
Run the following commands to capture the 'PhysicalResourceId' for the applicable components, as environment variables.

.. code-block::

    export EX010_SUBNET_PRIV1=$(aws cloudformation describe-stack-resources --stack-name ex-010 --output text --query 'StackResources[?LogicalResourceId==`SubnetPrivate1`].PhysicalResourceId')

    export EX010_SUBNET_PRIV2=$(aws cloudformation describe-stack-resources --stack-name ex-010 --output text --query 'StackResources[?LogicalResourceId==`SubnetPrivate2`].PhysicalResourceId')

    export EX010_SG_RDS=$(aws cloudformation describe-stack-resources --stack-name ex-010 --output text --query 'StackResources[?LogicalResourceId==`SecurityGroupRds`].PhysicalResourceId')

Sanity check
~~~~~~~~~~~~

.. code-block::
    
    echo -e '\n'$EX010_SUBNET_PRIV1'\n'$EX010_SUBNET_PRIV2'\n'$EX010_SG_RDS



Create a DB Subnet Group
------------------------

.. code-block::

    aws rds create-db-subnet-group \
        --db-subnet-group-name subnet_grp_ex010 \
        --db-subnet-group-description "Subnet group for ex-010" \
        --subnet-ids $EX010_SUBNET_PRIV1 $EX010_SUBNET_PRIV2

Output:

.. code-block::

    {
        "DBSubnetGroup": {
            "DBSubnetGroupName": "subnet_grp_ex010",
            "DBSubnetGroupDescription": "Subnet group for ex-010",
            "VpcId": "vpc-0850e7f16ce7f1b5a",
            "SubnetGroupStatus": "Complete",
            "Subnets": [
                {
                    "SubnetIdentifier": "subnet-006ab0717bdb18170",
                    "SubnetAvailabilityZone": {
                        "Name": "us-east-1b"
                    },
                    "SubnetStatus": "Active"
                },
                {
                    "SubnetIdentifier": "subnet-09b426c07ac3f155a",
                    "SubnetAvailabilityZone": {
                        "Name": "us-east-1a"
                    },
                    "SubnetStatus": "Active"
                }
            ],
            "DBSubnetGroupArn": "arn:aws:rds:us-east-1:926075045128:subgrp:subnet_grp_ex010"
        }
    }



.. code-block::

    aws rds create-db-instance \
        --db-instance-identifier db-ex-010 \
        --db-instance-class db.t2.micro \
        --storage-type gp2 \
        --allocated-storage 20 \
        --engine mysql \
        --master-username root \
        --master-user-password password \
        --vpc-security-group-ids $EX010_SG_RDS \
        --db-subnet-group-name subnet_grp_ex010 \
        --no-publicly-accessible

Output:

.. code-block::

    {
        "DBInstance": {
            "DBInstanceIdentifier": "db-ex-010a",
            "DBInstanceClass": "db.t2.micro",
            "Engine": "mysql",
            "DBInstanceStatus": "creating",
            "MasterUsername": "root",
            "AllocatedStorage": 20,
            "PreferredBackupWindow": "09:25-09:55",
            "BackupRetentionPeriod": 1,
            "DBSecurityGroups": [],
            "VpcSecurityGroups": [
                {
                    "VpcSecurityGroupId": "sg-0582c7bc25a2f5829",
                    "Status": "active"
                }
            ],
            "DBParameterGroups": [
                {
                    "DBParameterGroupName": "default.mysql5.6",
                    "ParameterApplyStatus": "in-sync"
                }
            ],
            "DBSubnetGroup": {
                "DBSubnetGroupName": "subnet_grp_ex010",
                "DBSubnetGroupDescription": "Subnet group for ex-010",
                "VpcId": "vpc-0850e7f16ce7f1b5a",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetIdentifier": "subnet-006ab0717bdb18170",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1b"
                        },
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-09b426c07ac3f155a",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1a"
                        },
                        "SubnetStatus": "Active"
                    }
                ]
            },
            "PreferredMaintenanceWindow": "fri:03:54-fri:04:24",
            "PendingModifiedValues": {
                "MasterUserPassword": "****"
            },
            "MultiAZ": false,
            "EngineVersion": "5.6.39",
            "AutoMinorVersionUpgrade": true,
            "ReadReplicaDBInstanceIdentifiers": [],
            "LicenseModel": "general-public-license",
            "OptionGroupMemberships": [
                {
                    "OptionGroupName": "default:mysql-5-6",
                    "Status": "in-sync"
                }
            ],
            "PubliclyAccessible": false,
            "StorageType": "gp2",
            "DbInstancePort": 0,
            "StorageEncrypted": false,
            "DbiResourceId": "db-SHVVNZK6EH6UWTQFGJ653T773Q",
            "CACertificateIdentifier": "rds-ca-2015",
            "DomainMemberships": [],
            "CopyTagsToSnapshot": false,
            "MonitoringInterval": 0,
            "DBInstanceArn": "arn:aws:rds:us-east-1:926075045128:db:db-ex-010a",
            "IAMDatabaseAuthenticationEnabled": false,
            "PerformanceInsightsEnabled": false
        }
    }




.. code-block::

    aws rds describe-db-instances \
        --db-instance-identifier db-ex-010 \
        --output text \
        --query DBInstances[*].DBInstanceStatus

Output:

.. code-block::

    creating




.. code-block::

    aws rds  modify-db-instance \
        --db-instance-identifier db-ex-010a \
        --multi-az \
        --apply-immediately

Output:

.. code-block::

    {
        "DBInstance": {
            "DBInstanceIdentifier": "db-ex-010a",
            "DBInstanceClass": "db.t2.micro",
            "Engine": "mysql",
            "DBInstanceStatus": "available",
            "MasterUsername": "root",
            "Endpoint": {
                "Address": "db-ex-010a.c13wv22kylew.us-east-1.rds.amazonaws.com",
                "Port": 3306,
                "HostedZoneId": "Z2R2ITUGPM61AM"
            },
            "AllocatedStorage": 20,
            "InstanceCreateTime": "2018-07-04T14:13:54.557Z",
            "PreferredBackupWindow": "09:25-09:55",
            "BackupRetentionPeriod": 1,
            "DBSecurityGroups": [],
            "VpcSecurityGroups": [
                {
                    "VpcSecurityGroupId": "sg-0582c7bc25a2f5829",
                    "Status": "active"
                }
            ],
            "DBParameterGroups": [
                {
                    "DBParameterGroupName": "default.mysql5.6",
                    "ParameterApplyStatus": "in-sync"
                }
            ],
            "AvailabilityZone": "us-east-1a",
            "DBSubnetGroup": {
                "DBSubnetGroupName": "subnet_grp_ex010",
                "DBSubnetGroupDescription": "Subnet group for ex-010",
                "VpcId": "vpc-0850e7f16ce7f1b5a",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetIdentifier": "subnet-006ab0717bdb18170",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1b"
                        },
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-09b426c07ac3f155a",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1a"
                        },
                        "SubnetStatus": "Active"
                    }
                ]
            },
            "PreferredMaintenanceWindow": "fri:03:54-fri:04:24",
            "PendingModifiedValues": {
                "MultiAZ": true
            },
            "LatestRestorableTime": "2018-07-04T23:30:00Z",
            "MultiAZ": false,
            "EngineVersion": "5.6.39",
            "AutoMinorVersionUpgrade": true,
            "ReadReplicaDBInstanceIdentifiers": [],
            "LicenseModel": "general-public-license",
            "OptionGroupMemberships": [
                {
                    "OptionGroupName": "default:mysql-5-6",
                    "Status": "in-sync"
                }
            ],
            "PubliclyAccessible": false,
            "StorageType": "gp2",
            "DbInstancePort": 0,
            "StorageEncrypted": false,
      
          "DbiResourceId": "db-SHVVNZK6EH6UWTQFGJ653T773Q",
            "CACertificateIdentifier": "rds-ca-2015",
            "DomainMemberships": [],
            "CopyTagsToSnapshot": false,
            "MonitoringInterval": 0,
            "DBInstanceArn": "arn:aws:rds:us-east-1:926075045128:db:db-ex-010a",
            "IAMDatabaseAuthenticationEnabled": false,
            "PerformanceInsightsEnabled": false
        }
    }


.. code-block::

    aws rds describe-db-instances \
        --db-instance-identifier db-ex-010a \
        --output table \
        --query 'DBInstances[*].{MultiAZ: MultiAZ,DBInstanceStatus: DBInstanceStatus}'

Output:

.. code-block::

    ---------------------------------
    |      DescribeDBInstances      |
    +-------------------+-----------+
    | DBInstanceStatus  |  MultiAZ  |
    +-------------------+-----------+
    |  modifying        |  False    |
    +-------------------+-----------+





.. code-block::

    aws rds reboot-db-instance --db-instance-identifier db-ex-010a --force-failover

Output:

.. code-block::

    {
        "DBInstance": {
            "DBInstanceIdentifier": "db-ex-010a",
            "DBInstanceClass": "db.t2.micro",
            "Engine": "mysql",
            "DBInstanceStatus": "rebooting",
            "MasterUsername": "root",
            "Endpoint": {
                "Address": "db-ex-010a.c13wv22kylew.us-east-1.rds.amazonaws.com",
                "Port": 3306,
                "HostedZoneId": "Z2R2ITUGPM61AM"
            },
            "AllocatedStorage": 20,
            "InstanceCreateTime": "2018-07-04T14:13:54.557Z",
            "PreferredBackupWindow": "09:25-09:55",
            "BackupRetentionPeriod": 1,
            "DBSecurityGroups": [],
            "VpcSecurityGroups": [
                {
                    "VpcSecurityGroupId": "sg-0582c7bc25a2f5829",
                    "Status": "active"
                }
            ],
            "DBParameterGroups": [
                {
                    "DBParameterGroupName": "default.mysql5.6",
                    "ParameterApplyStatus": "in-sync"
                }
            ],
            "AvailabilityZone": "us-east-1a",
            "DBSubnetGroup": {
                "DBSubnetGroupName": "subnet_grp_ex010",
                "DBSubnetGroupDescription": "Subnet group for ex-010",
                "VpcId": "vpc-0850e7f16ce7f1b5a",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetIdentifier": "subnet-006ab0717bdb18170",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1b"
                        },
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-09b426c07ac3f155a",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1a"
                        },
                        "SubnetStatus": "Active"
                    }
                ]
            },
            "PreferredMaintenanceWindow": "fri:03:54-fri:04:24",
            "PendingModifiedValues": {},
            "LatestRestorableTime": "2018-07-05T00:15:00Z",
            "MultiAZ": true,
            "EngineVersion": "5.6.39",
            "AutoMinorVersionUpgrade": true,
            "ReadReplicaDBInstanceIdentifiers": [],
            "LicenseModel": "general-public-license",
            "OptionGroupMemberships": [
                {
                    "OptionGroupName": "default:mysql-5-6",
                    "Status": "in-sync"
                }
            ],
            "SecondaryAvailabilityZone": "us-east-1b",
            "PubliclyAccessible": false,
            "StorageType": "gp2",
            "DbInstancePort": 0,
            "StorageEncrypted": false,
            "DbiResourceId": "db-SHVVNZK6EH6UWTQFGJ653T773Q",
            "CACertificateIdentifier": "rds-ca-2015",
            "DomainMemberships": [],
            "CopyTagsToSnapshot": false,
            "MonitoringInterval": 0,
            "DBInstanceArn": "arn:aws:rds:us-east-1:926075045128:db:db-ex-010a",
            "IAMDatabaseAuthenticationEnabled": false,
            "PerformanceInsightsEnabled": false
        }
    }

.. code-block::
    aws rds describe-events --source-identifier db-ex-010a --source-type db-instance




.. code-block::

    aws rds modify-db-instance \
        --db-instance-identifier db-ex-010a \
        --no-multi-az \
        --apply-immediately

Output:

.. code-block::

    {
        "DBInstance": {
            "DBInstanceIdentifier": "db-ex-010a",
            "DBInstanceClass": "db.t2.micro",
            "Engine": "mysql",
            "DBInstanceStatus": "available",
            "MasterUsername": "root",
            "Endpoint": {
                "Address": "db-ex-010a.c13wv22kylew.us-east-1.rds.amazonaws.com",
                "Port": 3306,
                "HostedZoneId": "Z2R2ITUGPM61AM"
            },
            "AllocatedStorage": 20,
            "InstanceCreateTime": "2018-07-04T14:13:54.557Z",
            "PreferredBackupWindow": "09:25-09:55",
            "BackupRetentionPeriod": 1,
            "DBSecurityGroups": [],
            "VpcSecurityGroups": [
                {
                    "VpcSecurityGroupId": "sg-0582c7bc25a2f5829",
                    "Status": "active"
                }
            ],
            "DBParameterGroups": [
                {
                    "DBParameterGroupName": "default.mysql5.6",
                    "ParameterApplyStatus": "in-sync"
                }
            ],
            "AvailabilityZone": "us-east-1b",
            "DBSubnetGroup": {
                "DBSubnetGroupName": "subnet_grp_ex010",
                "DBSubnetGroupDescription": "Subnet group for ex-010",
                "VpcId": "vpc-0850e7f16ce7f1b5a",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetIdentifier": "subnet-006ab0717bdb18170",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1b"
                        },
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-09b426c07ac3f155a",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1a"
                        },
                        "SubnetStatus": "Active"
                    }
                ]
            },
            "PreferredMaintenanceWindow": "fri:03:54-fri:04:24",
            "PendingModifiedValues": {
                "MultiAZ": false
            },
            "LatestRestorableTime": "2018-07-05T10:05:00Z",
            "MultiAZ": true,
            "EngineVersion": "5.6.39",
            "AutoMinorVersionUpgrade": true,
            "ReadReplicaDBInstanceIdentifiers": [],
            "LicenseModel": "general-public-license",
            "OptionGroupMemberships": [
                {
                    "OptionGroupName": "default:mysql-5-6",
                    "Status": "in-sync"
                }
            ],
            "SecondaryAvailabilityZone": "us-east-1a",
            "PubliclyAccessible": false,
            "StorageType": "gp2",
            "DbInstancePort": 0,
            "StorageEncrypted": false,
            "DbiResourceId": "db-SHVVNZK6EH6UWTQFGJ653T773Q",
            "CACertificateIdentifier": "rds-ca-2015",
            "DomainMemberships": [],
            "CopyTagsToSnapshot": false,
            "MonitoringInterval": 0,
            "DBInstanceArn": "arn:aws:rds:us-east-1:926075045128:db:db-ex-010a",
            "IAMDatabaseAuthenticationEnabled": false,
            "PerformanceInsightsEnabled": false
        }
    }

.. code-block::

    aws rds create-db-instance-read-replica \
        --db-instance-identifier dbro-ex-010 \
        --source-db-instance-identifier db-ex-010a

Output:

.. code-block::

    {
        "DBInstance": {
            "DBInstanceIdentifier": "dbro-ex-010",
            "DBInstanceClass": "db.t2.micro",
            "Engine": "mysql",
            "DBInstanceStatus": "creating",
            "MasterUsername": "root",
            "AllocatedStorage": 20,
            "PreferredBackupWindow": "09:25-09:55",
            "BackupRetentionPeriod": 0,
            "DBSecurityGroups": [],
            "VpcSecurityGroups": [
                {
                    "VpcSecurityGroupId": "sg-0582c7bc25a2f5829",
                    "Status": "active"
                }
            ],
            "DBParameterGroups": [
                {
                    "DBParameterGroupName": "default.mysql5.6",
                    "ParameterApplyStatus": "in-sync"
                }
            ],
            "DBSubnetGroup": {
                "DBSubnetGroupName": "subnet_grp_ex010",
                "DBSubnetGroupDescription": "Subnet group for ex-010",
                "VpcId": "vpc-0850e7f16ce7f1b5a",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetIdentifier": "subnet-006ab0717bdb18170",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1b"
                        },
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-09b426c07ac3f155a",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1a"
                        },
                        "SubnetStatus": "Active"
                    }
                ]
            },
            "PreferredMaintenanceWindow": "fri:03:54-fri:04:24",
            "PendingModifiedValues": {},
            "MultiAZ": false,
            "EngineVersion": "5.6.39",
            "AutoMinorVersionUpgrade": true,
            "ReadReplicaSourceDBInstanceIdentifier": "db-ex-010a",
            "ReadReplicaDBInstanceIdentifiers": [],
            "LicenseModel": "general-public-license",
            "OptionGroupMemberships": [
                {
                    "OptionGroupName": "default:mysql-5-6",
                    "Status": "pending-apply"
                }
            ],
            "PubliclyAccessible": false,
            "StorageType": "gp2",
            "DbInstancePort": 0,
            "StorageEncrypted": false,
            "DbiResourceId": "db-THZGEC7WBG4EKJZJUSJU2H5W6A",
            "CACertificateIdentifier": "rds-ca-2015",
            "DomainMemberships": [],
            "CopyTagsToSnapshot": false,
            "MonitoringInterval": 0,
            "DBInstanceArn": "arn:aws:rds:us-east-1:926075045128:db:dbro-ex-010",
            "IAMDatabaseAuthenticationEnabled": false,
            "PerformanceInsightsEnabled": false
        }
    }









apt install mysql-client

mysql -h $DBHOST -u dbadmin -p

export DBHOST=db-ex-010.c13wv22kylew.us-east-1.rds.amazonaws.com

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| innodb             |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)


mysql> create database test;
Query OK, 1 row affected (0.01 sec)


mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| innodb             |
| mysql              |
| performance_schema |
| sys                |
| test               |
+--------------------+
6 rows in set (0.00 sec)

mysql> use test;
Database changed


mysql> show tables;
Empty set (0.00 sec)




Summary
-------
- To be added

Next steps
----------
In `ex-011 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-011_GettingStartedAutoScaling.rst>`_, we will get started with Auto Scaling.

