
# Criando Infraestrutura na AWS com Python e CloudFormation

Um dos melhores conselhos em DevOps, diz que devemos desenvolver toda a `infraestrutura em código`, para assim poder rastrear as modificações realizadas na infraestrutura ou mesmo apenas reproduzi-lá com exatidão.

Assim devemos tornar cada item da infraestrutura um elemento descrito por uma linha de código fonte, podendo ser versionado, conhecendo o histórico de qualquer configuração, incluindo quem a propôs, quem aprovou e quando foi aplicado.

Dessa forma temos a nossa infraestrutura sendo desenvolvida de forma rápida, eficiente, confiável e segura. Outras vantagens como sua infraestrutura pode ser portável, reutilizável e compartilhável e facilmente testável.

A infraestrutura como código é uma prática importante a ser adotada se você quiser implementar o DevOps na sua organização. Além disso, ela permitirá que o seu time economize o tempo gasto com falhas e tarefas repetitivas e possa investi-lo em novos projetos para o aprimoramento dos produtos e serviços. Assim, você poderá tornar a sua organização de TI mais responsiva, colaborativa, mais rápida e, finalmente, mais inovadora.

Para realizar esse "sonho", temos duas soluções possíveis.

1. [TerraForm](https://www.terraform.io/): Solução OpenSource da empresa hashicorp, e funciona em multiCloud.
2. [CloudFormation](https://aws.amazon.com/pt/cloudformation/?sc_channel=PS&sc_campaign=acquisition_BR&sc_publisher=google&sc_medium=english_cloudformation_b&sc_content=cloudformation_e&sc_detail=cloudformation&sc_category=cloudformation&sc_segment=159751569489&sc_matchtype=e&sc_country=BR&s_kwcid=AL!4422!3!159751569489!e!!g!!cloudformation&ef_id=EAIaIQobChMI68T_7Pbf4AIVUj0MCh3rfQrlEAAYASAAEgJw9vD_BwE:G:s): Solução AWS para criação de infraestrutura exclusiva para AWS.

Nesse estudo, não estou fazendo juízo de valor, para escolher a melhor solução. Estou apenas testando uma possibilidade.

Portanto, vamos utilizar o `CloudFormation` juntamente com o `Python`. E as bibliotecas `Troposphere` para criação do `CloudFormation` e `boto3` para comunicação com a AWS.

A metologia utilizada foi explorar as bibliotecas de forma separadas e em seguida propor um problema que a solução envolva obrigatoriamente as duas libs.

## Troposphere

A biblioteca [Troposphere](https://github.com/cloudtools/troposphere) tem a proposta de criar uma descrição de `CloudFormation` através de chamadas Python.

Portanto, dessa forma podemos facilmente criar arquivos JSON ou YAML no padrão do AWS CloudFormation escrevendo tudo em código Python.

> O troposphere também inclui suporte para OpenStack

Para começarmos a explorar, vamos instalar o `Troposphere`.

```bash
pip install troposphere
```

 

###Exemplo de utilização

Vamos começar com um exemplo, bastante simples.

Vamos provisionar uma máquina no EC2:

```python

# Importa as libs

from troposphere import Ref, Template
import troposphere.ec2 as ec2

#Cria o template
t = Template()

# Cria uma instancia
instance = ec2.Instance("server1")
instance.ImageId = "ami-951945d0"
instance.InstanceType = "t1.micro"

 # Adiciona a instancia no recurso
t.add_resource(instance)

# Gera o cloudformation no formato json
print(t.to_json())

# Gera o cloudformation no formato yaml
print(t.to_yaml())

```

 

O ideal é sempre parametrizar a receita do cloudformation para pode ser utilizado para vários propósitos.

 

Um exemplo de utilização de parâmetros:

 

```python

# Importando as libs

from troposphere import Parameter, Ref, Template

from troposphere.rds import DBInstance, DBParameterGroup

 

# Cria um template

t = Template()

 

# Criando uma descricao para template

t.add_description(

    "AWS CloudFormation Sample Template RDS_with_DBParameterGroup: Sample "

    "template showing how to create an Amazon RDS Database Instance with "

    "a DBParameterGroup.**WARNING** This template creates an Amazon "

    "Relational Database Service database instance. You will be billed for "

    "the AWS resources used if you create a stack from this template.")

 

param1 = t.add_parameter(Parameter(

    "ServerName",

    NoEcho=True,

    Description="Digite o nome do servidor",

    Type="String",

    MinLength="1",

    MaxLength="16",

    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",

    ConstraintDescription=("Pode conter apenas letras e números.")

))

 

print(t.to_json())

```

Para salvar o cloudformation em um arquivo yaml, pode ser feito dessa forma:

 

```python

with open('cloudformation.yaml', 'w') as f:

    f.write(t.to_yaml())

```

 

Todos os recursos que você pode utilizar:

|AWS::AmazonMQ|AWS::ApiGateway|AWS::ApiGatewayV2|AWS::AppStream|AWS::AppSync|AWS::ApplicationAutoScaling|
|AWS::Athena|AWS::AutoScaling|AWS::AutoScalingPlans|AWS::Batch|AWS::Budgets|AWS::CertificateManager|
|AWS::Cloud9|AWS::CloudFormation|AWS::CloudFront|AWS::CloudTrail|AWS::CloudWatch|AWS::CodeBuild|
|AWS::CodeCommit|AWS::CodeDeploy|AWS::CodePipeline|AWS::Cognito|AWS::Config|AWS::DAX|
|AWS::DLM|AWS::DMS|AWS::DataPipeline|AWS::DirectoryService|AWS::DocDB|AWS::DynamoDB|
|AWS::EC2|AWS::ECR|AWS::ECS|AWS::EFS|AWS::EKS|AWS::EMR|
|AWS::ElastiCache|AWS::ElasticBeanstalk|AWS::ElasticLoadBalancing|AWS::ElasticLoadBalancingV2|AWS::Elasticsearch|AWS::Events|
|AWS::FSx|AWS::Glue|AWS::GuardDuty|AWS::IAM|AWS::Inspector|AWS::IoT|
|AWS::IoT1Click|AWS::IoTAnalytics|AWS::KMS|AWS::Kinesis|AWS::KinesisAnalytics|AWS::KinesisAnalyticsV2|
|AWS::KinesisFirehose|AWS::Lambda|AWS::Logs|AWS::Neptune|AWS::OpsWorks|AWS::OpsWorksCM|
|AWS::RDS|AWS::Redshift|AWS::Route53|AWS::Route53Resolver|AWS::S3|AWS::SDB|
|AWS::SES|AWS::SNS|AWS::SQS|AWS::SSM|AWS::SageMaker|AWS::SecretsManager|
|AWS::Serverless|AWS::ServiceCatalog|AWS::ServiceDiscovery|AWS::StepFunctions|AWS::WAF|AWS::WAFRegional|
|AWS::WorkSpaces|  | | | |


# Broto