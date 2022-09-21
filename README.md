# Sobre o projeto #

Este projeto é o repositório do laboratório realizado na live
entitulada **Usando AWS Lambda com SNS e EventBridge para Identificar novas EC2**, que ocorreu no Youtube dia 20/09/2022.

O principal objetivo foi utilizar o EventBridge, AWS Lambda com a linguagem Python e SNS para identificar e notificar por email quando uma nova instância é criada em uma região e, caso seja uma instância indesejada, vamos excluir a instância.

## Considerações ## 

O código disponível no arquivo **lambda_handler.py** é o mesmo criado durante a live.

Para fazer uso lembre-se de modificar o parâmetro **TargetArn** do **sns.publish**.

## Passos para seguir o laboratório ## 

1. Criar Lambda: detecta-ec2

2. Adiciona trigger EventBridge à função Lambda detecta-ec2:
	- Cria nova Rule
		- Rule Name: detecta-ec2
		- Rule Type: Event pattern
			- EC2
			- EC2 Instance State-change Notification

3. Testar se a Lambda está sendo executada.
    
    ``print("Estado do EC2 alterado: ")
    print(event)``

    Como testar? Criado uma nova EC2!

4. Criar primeira instância de teste na mesma região que os outros recursos estão sendo criados.

5. Observar log no Cloudwatch

	A Lambda executou 2 vezes? Tudo certo então.

6. Editar regra do EventBridge para executar Lambda apenas no 'pending'.

7. Criar segunda instância de teste na mesma região

8. Observar log no Cloudwatch
	
    A Lambda só deve executar 1 vez

9. Criar tópico SNS detecta-ec2
	- Registrar inscrição no tópico
	- Confirmar email
	- Guardar o ARN para utilizar no TargetArn

10. Dar permissões para a Lambda
	- Na role existente nas configurações de permissão da Lambda, adicionar nova policy: detecta-ec2
		- SNS: 
			- Write -> Publish
			- Resource -> Topic ARN
		- EC2: 
			- List -> DescribeInstances
			- Read -> DescribeTags
			- Write -> TerminateInstances
			- Resource -> All resources

11. Testar se Lambda tem acesso ao EC2 e SNS

Código para teste

``import json
import boto3

def lambda_handler(event, context):
    
    print("EC2 Criado: ")
    print(event)
    
    if event['detail']['state'] == 'pending':
        
        instance_id = event['detail']['instance-id']
        
        ec2 = boto3.resource('ec2')
        ec2instance = ec2.Instance(instance_id)
        instance_type = ec2instance.instance_type
        
        print("Obtendo dados da instância: ", ec2instance.instance_type)
        
        sns = boto3.client('sns')
        sns.publish (
              TargetArn = 'arn:aws:sns:us-east-2:930779231265:detecta-ec2',
              Subject='Teste Permissão',
              Message = 'Teste Permissão',
              MessageStructure = 'string'
          )
        
    
        response = ec2instance.terminate()
        
        print('Instância Terminada')
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
``

12. Implementar o código final de acordo com o fuxograma **Usando AWS Lambda com SNS e EventBridge para Identificar novas EC2.drawio.pdf**

Observe que o código deste repositório já está contemplando o fuxograma.