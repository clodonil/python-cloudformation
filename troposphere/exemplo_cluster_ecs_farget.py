from troposphere import Parameter, Ref, Template
from troposphere.ecs import (
    Cluster, Service, TaskDefinition,
    ContainerDefinition, NetworkConfiguration,
    AwsvpcConfiguration, PortMapping
)

t = Template()
t.add_version('2010-09-09')
t.add_parameter(Parameter(
    'Subnet',
    Type='AWS::EC2::Subnet::Id',
    Description='A VPC subnet ID for the container.',
))

clustername = t.add_parameter(Parameter(
    "ClusterName",
    NoEcho=False,
    Description="Nome do Projeto",
    Type="String",
    MinLength="1",
    MaxLength="16",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
    ConstraintDescription=("Letra e numero")
))

cluster = t.add_resource(Cluster(
    'Cluster'
))

task_definition = t.add_resource(TaskDefinition(
    'TaskDefinition',
    RequiresCompatibilities=['FARGATE'],
    Cpu='256',
    Memory='512',
    NetworkMode='awsvpc',
    ContainerDefinitions=[
        ContainerDefinition(
            Name='nginx',
            Image='nginx',
            Essential=True,
            PortMappings=[PortMapping(ContainerPort=80)]
        )
    ]
))

service = t.add_resource(Service(
    'NginxService',
    Cluster=Ref(cluster),
    DesiredCount=1,
    TaskDefinition=Ref(task_definition),
    LaunchType='FARGATE',
    NetworkConfiguration=NetworkConfiguration(
        AwsvpcConfiguration=AwsvpcConfiguration(
            Subnets=[Ref('Subnet')]
        )
    )
))

with open('exemplo_cluster.yaml', 'w') as f:
    f.write(t.to_yaml())