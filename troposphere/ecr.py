from troposphere import Template, Parameter
from troposphere.ecr import Repository
from awacs.aws import Allow, Policy, AWSPrincipal, Statement
import awacs.ecr as ecr
import awacs.iam as iam


t = Template()

t.add_description("Exemplo de utilizacao do ecr")
    
project_name = t.add_parameter(Parameter(
    "ProjetoName",
    NoEcho=True,
    Description="Nome do Projeto",
    Type="String",
    MinLength="1",
    MaxLength="16",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
    ConstraintDescription=("Letra e numero")
))

t.add_resource(
    Repository(
        'MyRepository',
        RepositoryName='test-repository',
        RepositoryPolicyText=Policy(
            Version='2008-10-17',
            Statement=[
                Statement(
                    Sid='AllowPushPull',
                    Effect=Allow,
                    Principal='*',
                    Action=[
                        ecr.GetDownloadUrlForLayer,
                        ecr.BatchGetImage,
                        ecr.BatchCheckLayerAvailability,
                        ecr.PutImage,
                        ecr.InitiateLayerUpload,
                        ecr.UploadLayerPart,
                        ecr.CompleteLayerUpload,
                    ],
                ),
            ]
        ),
    )
)

with open('exemplo_ecr.yaml', 'w') as f:
    f.write(t.to_yaml())