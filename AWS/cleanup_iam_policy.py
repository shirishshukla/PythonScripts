##
# Description: Lambda Function to auto delete IAM policies which are not attached to any iam role, users or groups.
# Prerequisite:
#   - Must run from AWS Lambda
#   - lambda iam role to have permission to list and delete iam policy
##

import boto3

FilterScope='Local'         # All: all policies, AWS: AWS managed policy, Local: customer managed policies
DelteUnattachedPolices=True # True: Delete unattached policies

# session
IAMC = boto3.client('iam')

def lambda_handler(event, context):
    try:
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
