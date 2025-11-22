import os
import boto3
from datetime import datetime, timezone
from utils import response

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def lambda_handler(event, context):
    """
    DELETE /products/{product_id}
    Marca un producto como no disponible (soft delete)
    """
    product_id = event['pathParameters']['product_id']
    
    # Verificar que existe
    result = table.get_item(Key={'product_id': product_id})
    if 'Item' not in result:
        return response(404, {'error': 'Producto no encontrado'})
    
    try:
        # Soft delete: marcar como no disponible
        updated = table.update_item(
            Key={'product_id': product_id},
            UpdateExpression='SET available = :false, updated_at = :now',
            ExpressionAttributeValues={
                ':false': False,
                ':now': datetime.now(timezone.utc).isoformat()
            },
            ReturnValues='ALL_NEW'
        )
        
        return response(200, {
            'success': True,
            'message': 'Producto desactivado exitosamente',
            'data': updated['Attributes']
        })
        
    except Exception as e:
        print(f"Error eliminando producto: {str(e)}")
        return response(500, {'error': 'Error al eliminar producto'})