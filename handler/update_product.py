import json
import os
import boto3
from datetime import datetime, timezone
from decimal import Decimal
from utils import response, validate_product_data

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def lambda_handler(event, context):
    """
    PUT /products/{product_id}
    Actualiza un producto existente
    """
    product_id = event['pathParameters']['product_id']
    
    try:
        body = json.loads(event.get('body', '{}'), parse_float=Decimal)
    except json.JSONDecodeError:
        return response(400, {'error': 'JSON inválido'})
    
    # Validar datos
    errors = validate_product_data(body, is_update=True)
    if errors:
        return response(400, {'error': 'Datos inválidos', 'details': errors})
    
    # Verificar que existe
    result = table.get_item(Key={'product_id': product_id})
    if 'Item' not in result:
        return response(404, {'error': 'Producto no encontrado'})
    
    # Construir expresión de actualización
    update_expr = "SET updated_at = :updated_at"
    expr_values = {':updated_at': datetime.now(timezone.utc).isoformat()}
    
    updatable_fields = ['name', 'description', 'price', 'category', 'image_url', 'available', 'tags']
    
    for field in updatable_fields:
        if field in body:
            update_expr += f", {field} = :{field}"
            value = body[field]
            if field == 'price':
                value = Decimal(str(value))
            elif field == 'category':
                value = value.lower()
            expr_values[f':{field}'] = value
    
    try:
        updated = table.update_item(
            Key={'product_id': product_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values,
            ReturnValues='ALL_NEW'
        )
        
        return response(200, {
            'success': True,
            'message': 'Producto actualizado exitosamente',
            'data': updated['Attributes']
        })
        
    except Exception as e:
        print(f"Error actualizando producto: {str(e)}")
        return response(500, {'error': 'Error al actualizar producto'})