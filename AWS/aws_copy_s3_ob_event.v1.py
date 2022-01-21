##
# Document:
#   - Copy all files present in one bucket folder to another within same or diff bucket.
#   - And delete from source bucket after successfull copy.
##
## Sample Input event
# { "srcBucket": "src-Bucket-name", "srcDirPath": "src/Dir/Path", "destBucket": "dest-Bucket-name", "destDirPath": "dest/Dir/Path"}

import boto3
import os

## Variables # here am coping to same bucket
# Source and destination Dir should end with / and must be folder

## S3 Sessions
S3C = boto3.client('s3')
S3R = boto3.resource('s3')

## Lambda Function
def lambda_handler(event, context):
    # Get Source Bucket and key name
    try:
        srcBucket  = event['srcBucket']
        srcDirPath = event['srcDirPath']
        destBucket  = event['destBucket']
        destDirPath = event['destDirPath']
        if not srcDirPath.endswith('/'):
            srcDirPath = srcDirPath+'/'
        if not destDirPath.endswith('/'):
            destDirPath = destDirPath+'/'
    except Exception as err:
        print("Error: " + str(err))

    srcFiles2Copy = S3C.list_objects_v2(Bucket=srcBucket,Prefix=srcDirPath) #Get list of all objects in src bucket dir
    if 'Contents' in srcFiles2Copy:
        srcFiles2Copy =  srcFiles2Copy['Contents']
        for obj in srcFiles2Copy:
            srcObjName = obj['Key'].split(srcDirPath)[-1]
            srcObjKey = obj['Key']
            destObjKey = destDirPath + srcObjName
            try:
                copy_s3_obj(srcBucket, destBucket, srcObjKey, destObjKey)
            except Exception as err:
                print("Failed Error: "+ str(err))
                pass
    else:
        print('Src Bucket Dir: s3://{}/{}  IS EMPTY.'.format(srcBucket, srcDirPath))


def copy_s3_obj(srcBucket, destBucket, srcObjKey, destObjKey):
    try:
        print('\n==> Copy: S3 Object \"s3://{0}/{2}\" to \"s3://{1}/{3}\" and delete from source.'.format(srcBucket, destBucket, srcObjKey, destObjKey))
        S3R.Bucket(destBucket).copy({'Bucket': srcBucket, 'Key': srcObjKey }, destObjKey)
        S3R.Object(srcBucket, srcObjKey).delete()
        print('Move Success..')
    except Exception as err:
        print("Failed Error: "+ str(err))
        pass


## call.. for testing
#event={ "srcBucket": "test-buket", "srcDirPath": "test/a", "destBucket": "test-buket-dest", "destDirPath": "test/b"}
#if __name__ == '__main__':
#    lambda_handler(event, 'context')


## EN
