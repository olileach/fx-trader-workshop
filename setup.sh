#!/bin/sh

clear
region=$(curl -s http://169.254.169.254/latest/meta-data/placement/region) 
aws lambda update-function-code \
--function-name fx-trade-results \
--zip-file fileb:///home/ec2-user/environment/fx-trader-workshop/fx-trade-results.zip \
--output text \
--region $region
account_id=$(aws sts get-caller-identity --query Account --output text)
sed -i "s/{account_id}/$account_id/g" ./fx-trader-workshop/fx-trader-example.py
sed -i "s/{region_name}/$region/g" ./fx-trader-workshop/fx-trader-example.py
aws s3 cp /home/ec2-user/environment/fx-trader-workshop/fx-trader-example.py s3://fx-trader-${account_id}-${region}-bucket/fx-trader-example/scripts/fx-trader-example.py
sudo yum remove python36 -y
sudo yum install python38 python38-pip -y
sudo python3 -m pip install boto3
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
echo "Unzipping awscliv2.zip to /tmp/cli"
unzip -o -q /tmp/awscliv2.zip -d /tmp/cli
echo "Updating AWS CLI using awscliv2.zip in /tmp/cli"
sudo /tmp/cli/aws/install --update
clear
export PYTHONPATH=/usr/bin/python3
echo alias python='/usr/bin/python3' >> ~/.bashrc
cp /home/ec2-user/environment/fx-trader-workshop/trade_executor.py /home/ec2-user/environment/trade_executor.py
echo " "
echo " "
echo "Rebooting environment to complete setup"
echo " "
sleep 3
sudo reboot