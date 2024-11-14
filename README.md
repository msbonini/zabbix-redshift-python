# zabbix-redshift-python
Monitoring using Zabbix to monitor metrics from Redshift using python to collect metrics from cloudwatch.

Attention ! 

This script has been tested on debian 12, for other operating systems check the correct installation command.

1 - Install dependencies on Debian 
apt install python3-boto3

Optional:

# Create a virtual environment
python -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Install boto3
pip install boto3

2 - Copy the redshift_stats.py file to the external scripts folder that is defined in the zabbix_server.conf file example directory:

/usr/lib/zabbix/externalscripts
