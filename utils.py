import json
from decimal import Decimal

def response(status_code, body):
    """Genera una respuesta HTTP estándar"""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(clean_decimals(body))
    }

def clean_decimals(obj):
    """Convierte Decimals a int/float para JSON"""
    if isinstance(obj, list):
        return [clean_decimals(i) for i in obj]
    if isinstance(obj, dict):
        return {k: clean_decimals(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

def validate_product_data(data, is_update=False):
    """Valida los datos de un producto"""
    errors = []
    
    if not is_update:
        required_fields = ['name', 'category', 'price']
        for field in required_fields:
            if field not in data:
                errors.append(f"Campo requerido: {field}")
    
    if 'price' in data:
        try:
            price = Decimal(str(data['price']))
            if price <= 0:
                errors.append("El precio debe ser mayor a 0")
        except:
            errors.append("Precio inválido")
    
    if 'category' in data:
        valid_categories = [
            'arroces', 'tallarines', 'chaufas', 
            'sopas', 'entradas', 'bebidas', 'postres'
        ]
        if data['category'].lower() not in valid_categories:
            errors.append(f"Categoría inválida. Válidas: {', '.join(valid_categories)}")
    
    return errors