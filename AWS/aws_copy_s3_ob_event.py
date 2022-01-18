##
# Document:
#   - Copy all files present in one bucket folder to another within same or diff bucket.
#   - And delete from source bucket after successfull copy.
##

import boto3

## Variables # here am coping to same bucket
# Source and destination Dir should end with / and must be folder
#src
srcBucket='mybucket1'
srcDirPath='dir1/a/'
#dest
destBucket='mybucket1'
destDirPath='dir2/b/'

## S3 Sessions
S3C = boto3.client('s3')
S3R = boto3.resource('s3')

## Lambda Function
def lambda_handler(event, context):
    # Get Source Bucket and key name
    try:
        srcBucketName  = event['Records'][0]['s3']['bucket']['name']
        srcKeyFile = event['Records'][0]['s3']['object']['key']
    except Exception as err:
        print("Error: " + str(err))

    srcKeyFileName = srcKeyFile.split('/')[-1]
    if srcBucket == srcBucketName and srcKeyFile.startswith(srcDirPath):
        try:
            dstFileKey=destDirPath+srcKeyFile.split(srcDirPath)[1]
            copy_s3_obj(srcBucket, destBucket, srcFileKey, dstFileKey) # within same bucket
        except Exception as err:
            print("Failed Error: "+ str(err))
            pass

def copy_s3_obj(srcBucket, destBucket, srcFileKey, dstFileKey):
    try:
        print('\n==> Copy: S3 Object \"s3://{0}/{2}\" to \"s3://{1}/{3}\" and delete from source.'.format(srcBucket, destBucket, srcFileKey, dstFileKey))
        S3R.Bucket(destBucket).copy({'Bucket': srcBucket, 'Key': srcFileKey }, dstFileKey)
        S3R.Object(srcBucket, srcFileKey).delete()
        print('Success..')
    except Exception as err:
        print("Failed Error: "+ str(err))
        pass


## call.. for testing
#if __name__ == '__main__':
#    lambda_handler('event', 'context')


## EN
