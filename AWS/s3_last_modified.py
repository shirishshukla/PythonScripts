##
# Description: Find all buckets which have no modifed objects since last [thresholdDays] days.
# Note:
#   - This will not list bucket if has any object modified in last [thresholdDays] days.
#   - Can pass thresholdDays as args to overwirite it .
#     $ python3 script.py 10
##

import sys
import boto3
from datetime import datetime, timedelta, timezone
nowUTC = datetime.utcnow()


s3c = boto3.client('s3')
s3r = boto3.resource('s3')

thresholdDays=int(sys.argv[1]) if len(sys.argv) > 1 else 90 # days

print('Threshold Days:', thresholdDays)

for bucket in s3c.list_buckets()['Buckets']:
    bucketName=bucket['Name']
    get_last_mod_keys = lambda obj: int(obj['LastModified'].strftime('%s'))
    s3keys = s3c.list_objects_v2(Bucket=bucketName)['Contents']
    latestModified = [obj['LastModified'] for obj in sorted(s3keys, key=get_last_mod_keys)][-1]
    daysSinceLastModified = (nowUTC.replace(tzinfo=timezone.utc) - latestModified).days
    if not thresholdDays or thresholdDays == 0:
        print('=> Bucket Name: {} | Last Modified On: {} | Days Before: {}'.format(bucketName, str(latestModified), str(daysSinceLastModified)))
    elif thresholdDays and daysSinceLastModified > thresholdDays:
        print('=> Bucket Name: {} | Last Modified On: {} | Days Before: {}'.format(bucketName, str(latestModified), str(daysSinceLastModified)))


#Output Sample:
# % Python3 "/Users/shirish/Desktop/_workMAC/Python/s3_last_modified.py"
#  Threshold Days: 90
#  Bucket: cf-templates-xxxxxxxx-us-west-2 | Last Modified on: 2020-07-10 02:25:13+00:00 | Days Before: 557
#  Bucket: bucket_sks1 | Last Modified on: 2020-04-21 04:44:23+00:00 | Days Before: 637
#  Bucket: bucket_sks1 | Last Modified on: 2020-04-22 15:55:00+00:00 | Days Before: 635
#  Bucket: bucket_sks3 | Last Modified on: 2020-05-05 04:45:09+00:00 | Days Before: 623
