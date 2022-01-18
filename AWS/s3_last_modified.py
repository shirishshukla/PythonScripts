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
    latestModified = [ {'obj_key': obj['Key'], 'mod_time': obj['LastModified']} for obj in sorted(s3keys, key=get_last_mod_keys)][-1]
    daysSinceLastModified = (nowUTC.replace(tzinfo=timezone.utc) - latestModified['mod_time']).days
    #print(daysSinceLastModified)
    if not thresholdDays or thresholdDays == 0:
        print('=> Bucket: {} | Last Modified Key: {} on {} | Days Before: {}'.format(bucketName, latestModified['obj_key'], str(latestModified['mod_time']), str(daysSinceLastModified)))
    elif thresholdDays and daysSinceLastModified > thresholdDays:
        print('=> Bucket: {} | Last Modified Key: {} on {} | Days Before: {}'.format(bucketName, latestModified['obj_key'], str(latestModified['mod_time']), str(daysSinceLastModified)))


#Output Sample:
# % Python3 "/Users/shirish/Desktop/_workMAC/Python/s3_last_modified.py" 0
# Threshold Days: 0
# => Bucket: cf-templates-xxxx-us-west-2 | Last Modified Key: 2020192aje-cft.yml on 2020-07-10 02:25:13+00:00 | Days Before: 557
# => Bucket: sks_bucket1 | Last Modified Key: generate.py on 2020-04-21 04:44:23+00:00 | Days Before: 637
# => Bucket: sks_bucket2 | Last Modified Key: artifacts/batch/buildartifacts/build-108.zip on 2020-04-22 15:55:00+00:00 | Days Before: 635
# => Bucket: sks_bucket3 | Last Modified Key: 25Apr2020/a/a2/a on 2022-01-18 14:19:01+00:00 | Days Before: 0
# => Bucket: sks_bucket4 | Last Modified Key: sks/test/test.py on 2020-05-05 04:45:09+00:00 | Days Before: 623
