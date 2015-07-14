#!/bin/bash

# Check for ansible tools, and attempt to install if not
yum install -y python-pip
pip install ansible
