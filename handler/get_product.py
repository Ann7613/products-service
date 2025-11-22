import os
import boto3
from utils import response

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def lambda_handler(event, context):
    """
    GET /products/{product_id}
    Obtiene un producto específico
    """
    product_id = event['pathParameters']['product_id']
    
    try:
        result = table.get_item(Key={'product_id': product_id})
        
        if 'Item' not in result:
            return response(404, {'error': 'Producto no encontrado'})
        
        return response(200, {
            'success': True,
            'data': result['Item']
        })
        
    except Exception as e:
        print(f"Error obteniendo producto: {str(e)}")
        return response(500, {'error': 'Error al obtener producto'})