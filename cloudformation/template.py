#!/usr/bin/env python
# Converted from IAM_Users_Groups_and_Policies.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from troposphere import (
    Base64, FindInMap, Join, Output, Parameter, Ref, Template
)

from troposphere.autoscaling import LaunchConfiguration
from troposphere.iam import InstanceProfile, PolicyType, Role

from awacs.aws import Allow, Policy, Principal, Statement
from awacs.sts import AssumeRole

t = Template()

t.add_description("AWS CloudFormation Template: IAM Roles for "
                  "https://github.com/shawnsi/aws-codedeploy-serf.")

SerfEncryptKey = t.add_parameter(Parameter(
    "SerfEncryptKey",
    Description="Base64 encoded encryption key for Serf cluster.",
    Type="String"
))

AmiId = t.add_parameter(Parameter(
    "AmiId",
    Type="String",
    Description="AMI for Serf instances"
))

KeyName = t.add_parameter(Parameter(
    "KeyName",
    Type="String",
    Description="Name of an existing EC2 KeyPair to enable SSH access",
    MinLength="1",
    AllowedPattern="[\x20-\x7E]*",
    MaxLength="255",
    ConstraintDescription="can contain only ASCII characters.",
))

SecurityGroup = t.add_parameter(Parameter(
    "SecurityGroup",
    Type="String",
    Description="Security group for Serf instances.",
))

t.add_mapping("Region2Principal", {
    'ap-northeast-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'ap-southeast-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'ap-southeast-2': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'cn-north-1': {
        'EC2Principal': 'ec2.amazonaws.com.cn',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com.cn'},
    'eu-central-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'eu-west-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'sa-east-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'us-east-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'us-west-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'us-west-2': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'}
    }
)

t.add_resource(Role(
    "SerfInstanceRole",
    AssumeRolePolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow, Action=[AssumeRole],
                Principal=Principal(
                    "Service", [
                        FindInMap(
                            "Region2Principal",
                            Ref("AWS::Region"), "EC2Principal")
                    ]
                )
            )
        ]
    ),
    Path="/"
))

t.add_resource(PolicyType(
    "CodedeployS3Policy",
    PolicyName="CodedeployS3Policy",
    PolicyDocument={
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:Get*",
                    "s3:List*"
                ],
                "Resource": [
                    "*",
                ]
            }
        ]
    },
    Roles=[Ref("SerfInstanceRole")]
))

t.add_resource(PolicyType(
    "SerfEC2Policy",
    PolicyName="SerfEC2Policy",
    PolicyDocument={
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:Describe*",
                    "autoscaling:Describe*"
                ],
                "Resource": [
                    "*",
                ]
            }
        ]
    },
    Roles=[Ref("SerfInstanceRole")]
))

t.add_resource(InstanceProfile(
    "SerfInstanceProfile",
    Path="/",
    Roles=[Ref("SerfInstanceRole")]
))

LaunchConfiguration = t.add_resource(LaunchConfiguration(
    "LaunchConfiguration",
    UserData=Base64(Join('', [
        "#!/bin/bash\n",
        "yum -y update\n",
        "yum install -y ruby\n",
        "yum install -y aws-cli\n",
        "cd /home/ec2-user\n",
        "aws s3 cp s3://aws-codedeploy-", Ref("AWS::Region"),
        "/latest/install . --region ", Ref("AWS::Region"), "\n",
        "chmod +x ./install\n",
        "./install auto\n",

        "# Setup Serf Encryption Key\n",
        "mkdir -p /etc/serf\n",
        "echo '{\"encrypt_key\": \"", Ref("SerfEncryptKey"),
        "\"}' > /etc/serf/key.json\n",
    ])),
    IamInstanceProfile=Ref("SerfInstanceProfile"),
    ImageId=Ref(AmiId),
    KeyName=Ref(KeyName),
    SecurityGroups=[Ref(SecurityGroup)],
    InstanceType="m3.medium",
))

t.add_output([
    Output(
        "LaunchConfiguration",
        Description="Serf launch configuration for use in autoscaling groups",
        Value=Ref(LaunchConfiguration)
    )
])

print(t.to_json())

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
