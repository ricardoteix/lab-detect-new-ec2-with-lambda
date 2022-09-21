import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    
    print("Estado do EC2 Alterado.")
    print(event)
    
    instance_id = event['detail']['instance-id']
    
    ec2 = boto3.resource('ec2')
    
    ec2_instance = ec2.Instance(instance_id)
    instance_type = ec2_instance.instance_type
    
    tem_tag = False
    
    for tag in ec2_instance.tags:
        if tag['Key'] == 'token' and tag['Value'] == '898755788':
            tem_tag = True
            break
    
    if tem_tag == True:
        assunto_sem_tag = 'AWS # Nova instância criada'
        mensagem_tem_tag = f'AWS # Nova instância criada. Type: {instance_type}'
    else:
        assunto_sem_tag = 'TOKEN NÃO IDENTIFICADO # AWS # Nova instância criada'
        mensagem_tem_tag = f'TOKEN NÃO IDENTIFICADO # AWS # Nova instância criada. Type: {instance_type}'
        
        ec2_instance.terminate()
        
    sns = boto3.client('sns')
    sns.publish(
        TargetArn='arn:aws:sns:us-west-2:9867864566:detecta-ec2',
        Subject=assunto_sem_tag,
        Message=mensagem_tem_tag,
        MessageStructure='string'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
