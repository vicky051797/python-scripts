import re
import boto3
access_key = ''
secret_key = ''

client = boto3.client('iam',aws_access_key_id=access_key,aws_secret_access_key=secret_key)
users = client.list_users()

iam_user=[]
iam_policies={}
for key in users['Users']:
    iam_user.append(key['UserName'])

for usr in iam_user:
    user_groups = client.list_groups_for_user(UserName=usr)
    get_user_group = user_groups["Groups"]
    for group in get_user_group:
        group_name = group["GroupName"]
        response = client.list_attached_group_policies(GroupName=group_name)
        get_goup_policy = response["AttachedPolicies"]
        for group_policy in get_goup_policy:
            group_policy_name = group_policy['PolicyName']
            if group_policy_name in iam_policies:
                iam_policies[group_policy_name].append(usr)
            else:
                iam_policies[group_policy_name] = [usr]                

    List_of_Policies =  client.list_attached_user_policies(UserName=usr)
    get_user_policy = List_of_Policies["AttachedPolicies"]

    for policy in get_user_policy:
        policy_name = policy['PolicyName']
        if policy_name in iam_policies:
            iam_policies[policy_name].append(usr)
        else:
            iam_policies[policy_name] = [usr]


print(iam_policies)

