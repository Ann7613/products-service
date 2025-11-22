import json
import os
import uuid
import boto3
from datetime import datetime, timezone
from decimal import Decimal
from utils import response, validate_product_data

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def lambda_handler(event, context):
    """
    POST /products
    Crea un nuevo producto en el menú
    """
    try:
        body = json.loads(event.get('body', '{}'), parse_float=Decimal)
    except json.JSONDecodeError:
        return response(400, {'error': 'JSON inválido'})
    
    # Validar datos
    errors = validate_product_data(body)
    if errors:
        return response(400, {'error': 'Datos inválidos', 'details': errors})
    
    # Crear producto
    product_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    product = {
        'product_id': product_id,
        'name': body['name'],
        'category': body['category'].lower(),
        'description': body.get('description', ''),
        'price': Decimal(str(body['price'])),
        'image_url': body.get('image_url', ''),
        'available': body.get('available', True),
        'tags': body.get('tags', []),
        'created_at': now,
        'updated_at': now
    }
    
    try:
        table.put_item(Item=product)
        return response(201, {
            'success': True,
            'message': 'Producto creado exitosamente',
            'data': product
        })
    except Exception as e:
        print(f"Error creando producto: {str(e)}")
        return response(500, {'error': 'Error al crear producto'})