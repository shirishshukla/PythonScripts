##
# description: Create ami of instance
# this will create ami with
# name: instance_name-YYYMMDD.HHMM
#### howto
# sh script.sh instance-id
# eg.
# sh script.sh i-234567689

##

instanceID=$1
[[ -z $instanceID ]] && echo "Please pass instance id as arg" && exit 1

TODAY=`date +%Y%m%d.%H%M`

echo -e "----------------------------- $TODAY ---------------------------------"
instance_name=$(aws ec2 describe-instances --instance-ids $instanceID --query 'Reservations[].Instances[].[Tags[?Key==`Name`].Value[]]' --output text)
if [[ $instance_name == "" ]]; then
    echo -e "Instance-ID ($instanceID) doesn't exist. Please check."
    exit
else
    #Create the AMI name.
    ami_name="${instance_name}-${TODAY}"

    #To create AMI from the instance
    ami_id=$(aws ec2 create-image --instance-id "$instanceID" --name "$ami_name" --description "Auto AMI from $instance_name ($instanceID)" --no-reboot --output text)

    #Tag the AMI
    if [[ ! -z $ami_id ]]; then
        echo -e "\n==> AMI: $ami_id ($ami_name) created successfully from $instance_name ($instanceID).\n"
        aws ec2 create-tags --resources $ami_id --tags Key=Instance_id,Value=$instanceID Key=AMI_Creation_Date,Value=$TODAY
    else
        echo -e "\n==>FAILED: AMI creation failed from $instance_name ($instanceID). Please check.\n"
    fi
fi
