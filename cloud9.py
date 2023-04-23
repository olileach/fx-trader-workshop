import boto3
client = boto3.client('cloud9', region_name='eu-central-1')

envs=[]
arn=None

# Get list of all cloud9 environments
res_envs=client.list_environments()
for k in res_envs['environmentIds']:
    envs.append(k)

# loop  of all cloud9 environments
for env in envs:
  res = client.describe_environments(
      environmentIds=[
          env
      ]
  )
  for env in res['environments']:
    print(env['arn'])
    arn=env['arn']
  
    response = client.list_tags_for_resource(
      ResourceARN=arn
    )
    l=response['Tags']

    if any('cloud9-instance' in d.values() for d in l):
      break