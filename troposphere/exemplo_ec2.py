from troposphere import Ref, Template
import troposphere.ec2 as ec2
t = Template()
instance = ec2.Instance("myinstance")
instance.ImageId = "ami-951945d0"
instance.InstanceType = "t1.micro"
t.add_resource(instance)

with open('exemplo_ec2.yaml', 'w') as f:
    f.write(t.to_yaml())