#!/usr/bin/python3
import datetime
import sys
from optparse import OptionParser
import boto3
import json

### Arguments
parser = OptionParser()
parser.add_option("-i", "--cluster-id", dest="cluster_id",
                help="Redshift Cluster Identifier")
parser.add_option("-a", "--access-key", dest="access_key", default="",
                help="AWS Access Key")
parser.add_option("-k", "--secret-key", dest="secret_key", default="",
                help="AWS Secret Access Key")
parser.add_option("-r", "--region", dest="region", default="",
                help="AWS region")

(options, args) = parser.parse_args()

if (options.cluster_id == None):
    parser.error("-i Redshift Cluster Identifier is required")

if not options.access_key or not options.secret_key:
    use_roles = True
else:
    use_roles = False

### Real code
metrics = {
    "CPUUtilization": {"type": "float", "value": None},
    "DatabaseConnections": {"type": "int", "value": None},
    "HealthStatus": {"type": "int", "value": None},
    "MaintenanceMode": {"type": "int", "value": None},
    "ReadIOPS": {"type": "int", "value": None},
    "WriteIOPS": {"type": "int", "value": None},
    "ReadLatency": {"type": "float", "value": None},
    "WriteLatency": {"type": "float", "value": None},
    "ReadThroughput": {"type": "float", "value": None},
    "WriteThroughput": {"type": "float", "value": None},
    "NetworkReceiveThroughput": {"type": "float", "value": None},
    "NetworkTransmitThroughput": {"type": "float", "value": None},
    "PercentageDiskSpaceUsed": {"type": "float", "value": None}
}
end = datetime.datetime.utcnow()
start = end - datetime.timedelta(minutes=5)

if use_roles:
    conn = boto3.client('cloudwatch', region_name=options.region)
else:
    conn = boto3.client('cloudwatch', aws_access_key_id=options.access_key, aws_secret_access_key=options.secret_key, region_name=options.region)

results = {}

for metric, details in metrics.items():
    try:
        res = conn.get_metric_statistics(
            Namespace="AWS/Redshift",
            MetricName=metric,
            Dimensions=[{'Name': "ClusterIdentifier", 'Value': options.cluster_id}],
            StartTime=start,
            EndTime=end,
            Period=60,
            Statistics=["Average"]
        )
        datapoints = res.get('Datapoints')
        if len(datapoints) > 0:
            average = datapoints[-1].get('Average')
            if details["type"] == "float":
                results[metric] = "%.4f" % average
            elif details["type"] == "int":
                results[metric] = "%i" % average
        else:
            results[metric] = None
    except Exception as e:
        results[metric] = str(e)

print(json.dumps(results))