import boto3

# Datos de configuración
account_id = '297009612081'
dashboard_id = '09481f25-820f-476b-b351-a3f47b9901e6'
region = 'us-east-1'
qs_user = 'AWSReservedSSO_AdministratorAccess_84fc8e51a827a37b/JesusMartinez'  # Este usuario debe estar creado en QS
namespace = 'default'

# Cliente boto3
client = boto3.client('quicksight', region_name=region)

# ARN del usuario registrado
user_arn = f"arn:aws:quicksight:{region}:{account_id}:user/{namespace}/{qs_user}"

# Generar la URL
response = client.generate_embed_url_for_registered_user(
    AwsAccountId=account_id,
    SessionLifetimeInMinutes=60,
    UserArn=user_arn,
    ExperienceConfiguration={
        'Dashboard': {
            'InitialDashboardId': dashboard_id
        }
    }
)

print("URL de embed:", response['EmbedUrl'])
