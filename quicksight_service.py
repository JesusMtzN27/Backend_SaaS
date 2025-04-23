# quicksight_service.py
import boto3
from botocore.exceptions import ClientError
from config import AWS_ACCOUNT_ID, AWS_REGION, DASHBOARD_ID, NAMESPACE  # Importar las credenciales desde config.py

def get_quicksight_embed_url(username, report_name):
    """
    Genera la URL de incrustación de un reporte de Amazon QuickSight
    filtrado por el nombre de usuario para Row-Level Security (RLS).
    
    Args:
    - username: Nombre del usuario (se usa para RLS).
    - report_name: El nombre del reporte a incrustar.

    Returns:
    - Embed URL de QuickSight o un mensaje de error si ocurre un problema.
    """
    try:
        # Configura el cliente de AWS QuickSight con las credenciales del archivo de configuración
        quicksight_client = boto3.client('quicksight', region_name=AWS_REGION)

        # Generar la URL de incrustación
        response = quicksight_client.get_dashboard_embed_url(
            AwsAccountId=AWS_ACCOUNT_ID,
            DashboardId=DASHBOARD_ID,  # Usar el ID del dashboard
            IdentityType='IAM',
            SessionAttributes={'username': username},  # Filtro por el nombre de usuario para RLS
            ResetDisabled=True,
            UndoRedoDisabled=True
        )

        # Devolver la URL de incrustación
        return response['EmbedUrl']

    except ClientError as e:
        print(f"Error al generar la URL de incrustación: {e}")
        return None
