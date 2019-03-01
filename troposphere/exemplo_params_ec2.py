
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
    f.write(t.to_yaml())