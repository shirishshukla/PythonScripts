##
# Document:
#   - Copy LATEST files present in one bucket folder to another within same or diff bucket.
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
        # ensure src and dst dir in desired format
        if srcDirPath.startswith('/'):     srcDirPath = srcDirPath[1:]
        if destDirPath.startswith('/'):    destDirPath = destDirPath[1:]
        if not srcDirPath.endswith('/'):   srcDirPath = srcDirPath+'/'
        if not destDirPath.endswith('/'):  destDirPath = destDirPath+'/'
        # get latest modified obj in src bucket
        latestModFile= get_latest_modified_obj(srcBucket, srcDirPath)
        if latestModFile:
            srcObjName = latestModFile.split(srcDirPath)[-1]
            srcObjKey = latestModFile
            destObjKey = destDirPath + srcObjName
            copy_s3_obj(srcBucket, destBucket, srcObjKey, destObjKey)
    except Exception as err:
        print("Error: " + str(err))


# Get Latest modifed obj in S3 bucket
def get_latest_modified_obj(srcBucket, srcDirPath):
    try:
        get_last_mod_keys = lambda obj: int(obj['LastModified'].strftime('%s'))
        s3keys = S3C.list_objects_v2(Bucket=srcBucket,Prefix=srcDirPath) # GET LIST OF ALL OBECTS IN SRC BUCKET
        if 'Contents' in s3keys:
            s3keys = s3keys['Contents']
            latestModFile = [ {'obj_key': obj['Key'], 'mod_time': obj['LastModified']} for obj in sorted(s3keys, key=get_last_mod_keys)][-1] ## GET LAST MODIFIED FILE.
            print("Bucket: {}, Latest modified Object {}, At Time: {}".format(srcBucket, latestModFile['obj_key'], latestModFile['mod_time']))
            return latestModFile['obj_key']
        else:
            print('Src Bucket Dir: s3://{}/{}, IS EMPTY.'.format(srcBucket, srcDirPath))
    except Exception as err:
        print("Failed Error: "+ str(err))
        pass
    return False

# Copy obj from src biucket to dest and del from src
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
