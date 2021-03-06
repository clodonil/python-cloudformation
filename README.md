
# Criando Infraestrutura na AWS com Python e CloudFormation

Um dos melhores conselhos em DevOps, diz que devemos desenvolver toda a `infraestrutura em código`, para assim poder rastrear as modificações realizadas na infraestrutura ou mesmo apenas reproduzi-lá com exatidão.

Assim devemos tornar cada item da infraestrutura um elemento descrito por uma linha de código fonte, podendo ser versionado, conhecendo o histórico de qualquer configuração, incluindo quem a propôs, quem aprovou e quando foi aplicado.

Dessa forma temos a nossa infraestrutura sendo desenvolvida de forma rápida, eficiente, confiável e segura. Outras vantagens como sua infraestrutura pode ser portável, reutilizável e compartilhável e facilmente testável.

A infraestrutura como código é uma prática importante a ser adotada se você quiser implementar o DevOps na sua organização. Além disso, ela permitirá que o seu time economize o tempo gasto com falhas e tarefas repetitivas e possa investi-lo em novos projetos para o aprimoramento dos produtos e serviços. 

Assim, você poderá tornar a sua organização de TI mais responsiva, colaborativa, mais rápida e, finalmente, mais inovadora.

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

Vamos começar pelo exemplo mais simples possível em uma infraestrutura, que é a criação de um novo servidor. Para ficar claro, vamos utilizar a seguinte dinâmica:

1. Criar o código em Python;
2. Gerar o CloudFormation;
3. Criar um stack de CloudFormation na AWS;
4. Monitorar a execução.

Como pré-requisito para executar os exemplos a seguir é ter uma conta na AWS.

Vamos provisionar uma máquina no EC2, a explicação de cada linha coloquei no código.

```python
# Importa as libs
from troposphere import Ref, Template
import troposphere.ec2 as ec2

#Cria o template
t = Template()

# Cria uma instancia
# Define o nome da instancia
instance = ec2.Instance("server1")
# Define o tipo da imagem
instance.ImageId = "ami-951945d0"
# Define o tamanho da maquina
instance.InstanceType = "t1.micro"

 # Adiciona a instancia no recurso
t.add_resource(instance)

# Gera o cloudformation no formato json
print(t.to_json())

# Gera o cloudformation no formato yaml
print(t.to_yaml())

# Salva o arquivo exemplo_ecs.yaml no formato do cloudformation
with open('exemplo_ec2.yaml', 'w') as f:
    f.write(t.to_yaml())
```

Ao executar o programa acima, o arquivo `JSON` no formato do cloudformation é gerado e impresso na tela.

```json
{
    "Resources": {
        "server1": {
            "Properties": {
                "ImageId": "ami-951945d0",
                "InstanceType": "t1.micro"
            },
            "Type": "AWS::EC2::Instance"
        }
    }
}
```

também o modelo no formato `YAML`.

```yaml
Resources:
  server1:
    Properties:
      ImageId: ami-951945d0
      InstanceType: t1.micro
    Type: AWS::EC2::Instance
```

E a ultimas linhas do programa, salva o formato do `yaml` dentro do arquivo `exemplo_ecs2.yaml`.

Vamos utilizar esse arquivo para criar um `stack` na AWS com esse CloudFormation.

Podemos fazer isso utilizando o seguinte comando:

```bash
aws cloudformation create-stack --stack-name ec2-exemplo --template-body file://exemplo_ec2.yaml
```
 
A figura 1, mostra a `stack` criada e o CloudFormation executado com sucesso.

![ec2-exemplo](img/img1.png)

Se olhamos as instâncias podemos ver que foi criado o `server1` e o mesmo já esta em execução:

![ec2-exemplo-run](img/img2.png)

Uma boa prática é sempre parametrizar a receita do cloudformation para pode ser utilizado para vários propósitos.

Um exemplo de utilização de parâmetros:

```python

# Importando as libs
from troposphere import Parameter, Ref, Template
import troposphere.ec2 as ec2

# Cria um template
t = Template()

# Criando uma descricao para template
t.add_description("utilizando parametro com o nome do servidor")

servername = t.add_parameter(Parameter(
    "ServerName",
    NoEcho=True,
    Description="Digite o nome do servidor",
    Type="String",
    MinLength="1",
    MaxLength="16",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
    Default = "server1",
    ConstraintDescription=("Pode conter apenas letras e números.")
))

instance = ec2.Instance("server1")
# Define o tipo da imagem
instance.ImageId = "ami-951945d0"
# Define o tamanho da maquina
instance.InstanceType = "t1.micro"

 # Adiciona a instancia no recurso
t.add_resource(instance)

# Gera o cloudformation no formato json
print(t.to_json())

# Gera o cloudformation no formato yaml
print(t.to_yaml())

# Salva o arquivo exemplo_ecs.yaml no formato do cloudformation
with open('exemplo_params_ec2.yaml', 'w') as f:
    f.write(t.to_yaml())```

Segue o arquivo `YAML` criado pelo programa acima:

```yaml
Description: utilizando parametro com o nome do servidor
Parameters:
  ServerName:
    AllowedPattern: '[a-zA-Z][a-zA-Z0-9]*'
    ConstraintDescription: "Pode conter apenas letras e n\xFAmeros."
    Default: server1
    Description: Digite o nome do servidor
    MaxLength: '16'
    MinLength: '1'
    NoEcho: true
    Type: String
Resources:
  server1:
    Properties:
      ImageId: ami-951945d0
      InstanceType: t1.micro
    Type: AWS::EC2::Instance
```

Todos os recursos que você pode utilizar:

|||Opções de Recusos||
|:--|:--|:--|:--|
|AWS::AmazonMQ|AWS::ApiGateway|AWS::ApiGatewayV2|AWS::CloudWatch|
|AWS::Athena|AWS::AutoScaling|AWS::AutoScalingPlans|AWS::KinesisAnalyticsV2   |
|AWS::Cloud9|AWS::CloudFormation|AWS::CloudFront|AWS::CloudTrail|
|AWS::CodeCommit|AWS::CodeDeploy|AWS::CodePipeline|AWS::Cognito|
|AWS::DLM|AWS::DMS|AWS::DataPipeline|AWS::DirectoryService|
|AWS::EC2|AWS::ECR|AWS::ECS|AWS::EFS|
|AWS::ElastiCache|AWS::ElasticBeanstalk|AWS::ElasticLoadBalancing|AWS::ElasticLoadBalancingV2|
|AWS::FSx|AWS::Glue|AWS::GuardDuty|AWS::IAM|
|AWS::IoT1Click|AWS::IoTAnalytics|AWS::KMS|AWS::Kinesis|
|AWS::KinesisFirehose|AWS::Lambda|AWS::Logs|AWS::Neptune|
|AWS::RDS|AWS::Redshift|AWS::Route53|AWS::Route53Resolver|
|AWS::SES|AWS::SNS|AWS::SQS|AWS::SSM|
|AWS::Serverless|AWS::ServiceCatalog|AWS::ServiceDiscovery|AWS::StepFunctions|
|AWS::WorkSpaces|AWS::ApplicationAutoScaling  |AWS::CertificateManager |AWS::CodeBuild |
|AWS::DynamoDB|AWS::EKS|AWS::EMR|AWS::Events|AWS::IoT|
|AWS::SecretsManager|AWS::WAFRegional|AWS::OpsWorksCM|AWS::SDB|AWS::Elasticsearch|
|AWS::AppStream|AWS::AppSync |AWS::Batch|AWS::Budgets | 
|AWS::Config |AWS::DocDB |AWS::Inspector |AWS::S3 |
|AWS::KinesisAnalytics|AWS::OpsWorks |AWS::WAF | AWS::DAX |
|AWS::SageMaker |   | | |
# Broto