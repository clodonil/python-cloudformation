# Importa as libs
from troposphere import Ref, Template, Base64
import troposphere.ec2 as ec2

#Cria o template
t = Template()

# Cria uma instancia
# Define o nome da instancia
instance = ec2.Instance("server1")
# Define o tipo da imagem
instance.ImageId = "ami-09bfcadb25ee95bec"
# Define o tamanho da maquina
instance.InstanceType = "t2.micro"

 # Adiciona a instancia no recurso
t.add_resource(instance)

# Gera o cloudformation no formato json
print(t.to_json())

# Gera o cloudformation no formato yaml
print(t.to_yaml())

# Salva o arquivo exemplo_ecs.yaml no formato do cloudformation
with open('exemplo_ec2.yaml', 'w') as f:
    f.write(t.to_yaml())