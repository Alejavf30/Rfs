import os
import uuid
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkaos.v1 import AosClient, CreateStackRequest, CreateStackRequestBody, TemplateBodyPrimitiveTypeHolder
from huaweicloudsdkaos.v1.region.aos_region import AosRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

ak = "VYONFBJNIHEH2ARQDJSA"
sk = "zKSRz7T9tRmLPTQg9qAXt1OqKMk6wXUassP41nzJ"
project_id = "db258ca256a84146bfdf13b0a33671aa"  

# Para las llaves para conectarse a la API de Huawei CLOUD
config = HttpConfig.get_default_config()
config.ignore_ssl_verification = True
credentials = BasicCredentials(ak, sk)

# Crear un cliente para la VPC para interactuar con la API
client = AosClient.new_builder() \
    .with_credentials(credentials) \
    .with_http_config(config) \
    .with_region(AosRegion.value_of("ap-southeast-3")) .build()

# Para definir la plantilla del RFS
terraform_template = """
{
  "terraform": {
    "required_providers": {
      "huaweicloud": {
        "source": "huawei.com/provider/huaweicloud",
        "version": "1.56.0"
      }
    }
  },
  "provider": {
    "huaweicloud": {
      "insecure": true,
      "region": "ap-southeast-3"
    }
  },
  "resource": {
    "huaweicloud_vpc": {
      "vpc-l3i3d": {
        "name": "vpc4",
        "cidr": "10.0.0.0/8"
      }
    },
    "huaweicloud_vpc_subnet": {
      "vpc-subnet-qmel7": {
        "vpc_id": "${huaweicloud_vpc.vpc-l3i3d.id}",
        "name": "subnet1",
        "cidr": "10.0.0.0/8",
        "gateway_ip": "10.0.0.1"
      }
    }
  }
}
"""

# Para el create stack
stack_request_body = CreateStackRequestBody(
    stack_name="stack9",  # Nombre del stack
    template_body=terraform_template  # Plantilla HCL
)
client_request_id = str(uuid.uuid4())
try:
    create_request = CreateStackRequest(
        client_request_id=client_request_id,
        body=stack_request_body  
    )

    # Se enevia la solictud para crear el stack
    create_response = client.create_stack(create_request)
    print(f"Stack creado con éxito: {create_response}")

except exceptions.ClientRequestException as e:
    print(f"Error al crear el stack: {e.status_code}, {e.error_msg}")