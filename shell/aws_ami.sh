##
# Description: Create ami of AWS ec2 instance
#  This will create AMI with tags
#   - name: instance_name-YYYMMDD.HHMM
#   - Instance_id:
#   - AMI_Creation_Date:
#
#### !! How TO !!
# Syntax: sh script.sh instance-id
# eg.
#    sh script.sh i-234567689
##

instanceID=$1
[[ -z $instanceID ]] && echo "Please pass instance-id as arg" && exit 1

TODAY=`date +%Y%m%d.%H%M`

echo -e "-------------- Creating AMI of ec2 instance $instanceID --------------"
if `aws ec2 describe-instances --instance-ids $instanceID >/dev/null 2>&1`; then
    instance_name=$(aws ec2 describe-instances --instance-ids $instanceID --query 'Reservations[].Instances[].[Tags[?Key==`Name`].Value[]]' --output text)
    [[ -z $instance_name ]] && instance_name=$instanceID
else
    echo -e "Instance-ID ($instanceID) doesn't exist. Please check."
    exit 1
else
    # ami name
    ami_name="${instance_name}-${TODAY}"

    # create AMI from the instance
    ami_id=$(aws ec2 create-image --instance-id "$instanceID" --name "$ami_name" --description "Auto AMI from $instance_name ($instanceID)" --no-reboot --output text)

    # Tag the AMI with instance id and creation date
    if [[ ! -z $ami_id ]]; then
        echo -e "\n==> AMI: $ami_id ($ami_name) created successfully from $instance_name ($instanceID).\n"
        aws ec2 create-tags --resources $ami_id --tags Key=Name,Value=$ami_name Key=Instance_id,Value=$instanceID Key=AMI_Creation_Date,Value=$TODAY
    else
        echo -e "\n==> FAILED: AMI creation failed for instance $instance_name ($instanceID). Please check.\n"
    fi
fi
