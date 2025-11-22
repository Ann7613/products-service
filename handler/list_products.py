import os
import boto3
from utils import response

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def lambda_handler(event, context):
    """
    GET /products?available=true&category=arroces
    Lista productos con filtros opcionales
    """
    query_params = event.get('queryStringParameters') or {}
    available_filter = query_params.get('available')
    category_filter = query_params.get('category')
    
    try:
        # Scan completo (en producción usarías paginación)
        scan_result = table.scan()
        products = scan_result.get('Items', [])
        
        # Aplicar filtros
        if available_filter:
            is_available = available_filter.lower() == 'true'
            products = [p for p in products if p.get('available') == is_available]
        
        if category_filter:
            products = [p for p in products if p.get('category') == category_filter.lower()]
        
        # Ordenar por nombre
        products.sort(key=lambda x: x.get('name', ''))
        
        return response(200, {
            'success': True,
            'count': len(products),
            'data': products
        })
        
    except Exception as e:
        print(f"Error listando productos: {str(e)}")
        return response(500, {'error': 'Error al listar productos'})