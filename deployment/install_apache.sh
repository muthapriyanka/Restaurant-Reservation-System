#!/bin/bash

# Install Apache
sudo apt-get update
sudo apt-get install -y apache2

# Get token and pull instance id and public ipv4 from instance metadata
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
INSTANCE_ID=$(curl http://169.254.169.254/latest/meta-data/instance-id -H "X-aws-ec2-metadata-token: $TOKEN")                                           
INSTANCE_IP=$(curl http://169.254.169.254/latest/meta-data/public-ipv4 -H "X-aws-ec2-metadata-token: $TOKEN")



# echo to web page
echo "Hello world! My instance id is: $INSTANCE_ID and public ip is: $INSTANCE_IP" > index.html

sudo cp index.html /var/www/html
