##
# Description: Lambda Function to auto delete IAM policies which are not attached to any iam role, users or groups.
# Prerequisite:
#   - Must run from AWS Lambda
#   - lambda iam role to have permission to list and delete iam policy
#   input: event = { 'account': ['ac1', 'ac2'], 'action': 'delete'}
##

import boto3

FilterScope='Local'          # All: all policies, AWS: AWS managed policy, Local: customer managed policies
DelteUnattachedPolices=False # False: do not del as defualt
AssumeRoleName='assumeMe' ## change this ????

# session
STSC = boto3.client('sts')

# Lambda Function
def lambda_handler(event, context):
    try:
        AccountIds = event['accounts']
        DelteUnattachedPolices = True if 'action' in event and event['action'] == 'delete' else DelteUnattachedPolices
        if AccountIds:
            for act in AccountIds:
                roleARN = f"arn:aws:iam::{act}:role/{AssumeRoleName}"
                assume_role = STSC.assume_role(RoleArn=roleARN, RoleSessionName='assumme')['Credentials']
                IAMC = boto3.client('iam',
                        aws_access_key_id=assume_role['AccessKeyId']
                        aws_secret_access_key=assume_role['SecretAccessKey']
                        aws_session_token=assume_role['SessionToken']
                )
                POLICIES_DATA = IAMC.list_policies(
                        Scope=FilterScope,
                        OnlyAttached=False
                    )

                FILTERED_POLICIES = [ p['Arn'] for p in POLICIES_DATA['Policies'] if p['AttachmentCount'] == 0 ]
                while 'Marker' in POLICIES_DATA:
                    POLICIES_DATA = IAMClist_policies(
                            Scope=FilterScope,
                            OnlyAttached=False,
                            Marker=POLICIES_DATA['Marker']
                        )
                    FILTERED_POLICIES += [ p['Arn'] for p in POLICIES_DATA['Policies'] if p['AttachmentCount'] == 0 ]

                print(f'Total Policies Which Are Not attached to any iam role, group or users are: {len(FILTERED_POLICIES)}')
                if FILTERED_POLICIES:
                    for policyArn in FILTERED_POLICIES:
                        if DelteUnattachedPolices:
                            policyName = policyArn.split('/')[-1]
                            print(f"\n--> Deleting Policy: {policyName}")
                            try:
                                resp = IAMC.delete_policy(PolicyArn=policyArn)
                                print('Success: Successfully deleted policy')
                            except Exception as err:
                                print(f'FAILED: to delete policy: {policyName}')
                        else:
                            print(f'\nIgnore Policy: {policyName}')
                else:
                    print('No unattahced policy\'s exist!!')
    except Exception as err:
        print(f'FAILED: with error: {err}')


## END
