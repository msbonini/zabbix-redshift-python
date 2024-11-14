# Zabbix Monitoring AWS Redshift
Monitoring using Zabbix to monitor metrics from Redshift using python to collect metrics from cloudwatch.

# Compatibility: This monitoring is compatible with Zabbix 7.0 or higher

# Attention ! 
This script has been tested on debian 12, for other operating systems check the correct installation command.

# 1 - Install dependencies on Debian (No need to use virtual environment)
apt install python3-boto3

# Optional (Use of virtual environment):
Create a virtual environment
python -m venv myenv

Activate the virtual environment
source myenv/bin/activate

Install boto3
 
 pip install boto3

# 2 - Copy script python to folder external scripts
Copy the redshift_stats.py file to the external scripts folder that is defined in the zabbix_server.conf file example directory:

  Example:
  /usr/lib/zabbix/externalscripts

# 3 - Import Template on Zabbix
Import template into Zabbix

# 5 - Configure AWS credentials macros

{$AWS_ACCESS_KEY} - Access Key

{$AWS_REGION} - AWS region where the cluster is provisioned ex: us-east-1

{$AWS_SECRET_KEY} - Secret Key

# 4 - Create Host 
Within the host configuration, enter the name of the cluster exactly as it is registered in AWS. And in the host name, it is up to you to choose the most friendly name. Because the script will use the {HOST.HOST} macro within the item it collects, passing the name of the cluster into the script as an argument.

format: 	
redshift_stats.py["--cluster-id","{HOST.HOST}","--access-key","{$AWS_ACCESS_KEY}","--secret-key","{$AWS_SECRET_KEY}","--region","{$AWS_REGION}"]

# This model was based on the zabbix-cloudwatch project available at the link below:

https://github.com/omni-lchen/zabbix-cloudwatch/tree/master

Main Changes Implemented:

1. Bulk Data Collection: I developed a unique script that collects all metrics at once and feeds all dependent items simultaneously, optimizing the monitoring process.

2. Dependent Items: Items that previously ran the original script for each metric have been converted to dependent items. I used jsonpath to extract the corresponding values ​​for each item, improving efficiency.

3. Macro Names: I optimized the macro names to make triggers easier to understand and understand, making configuration more intuitive.

4. Units and History Retention: I corrected some units of measurement and adjusted history retention times to ensure the accuracy and relevance of monitored data.

5. Credentials via Macros: Access Key, Secret Key and Region credentials are now managed through macros within Zabbix, simplifying configuration and increasing security.
