import os
import boto3
from boto3.dynamodb.conditions import Key
from utils import response

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def lambda_handler(event, context):
    """
    GET /categories/{category}/products
    Obtiene productos por categoría usando GSI
    """
    category = event['pathParameters']['category'].lower()
    query_params = event.get('queryStringParameters') or {}
    available_only = query_params.get('available', 'true').lower() == 'true'
    
    try:
        # Query usando GSI CategoryIndex
        result = table.query(
            IndexName='CategoryIndex',
            KeyConditionExpression=Key('category').eq(category)
        )
        
        products = result.get('Items', [])
        
        # Filtrar por disponibilidad
        if available_only:
            products = [p for p in products if p.get('available', True)]
        
        return response(200, {
            'success': True,
            'category': category,
            'count': len(products),
            'data': products
        })
        
    except Exception as e:
        print(f"Error obteniendo productos por categoría: {str(e)}")
        return response(500, {'error': 'Error al obtener productos'})