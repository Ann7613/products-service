from utils import response

def lambda_handler(event, context):
    """
    GET /categories
    Lista todas las categorías disponibles
    """
    categories = [
        {
            'id': 'arroces',
            'name': 'Arroces',
            'description': 'Arroces chinos tradicionales',
            'icon': '🍚'
        },
        {
            'id': 'tallarines',
            'name': 'Tallarines',
            'description': 'Tallarines saltados y especiales',
            'icon': '🍜'
        },
        {
            'id': 'chaufas',
            'name': 'Chaufas',
            'description': 'Arroz chaufa en todas sus variedades',
            'icon': '🍛'
        },
        {
            'id': 'sopas',
            'name': 'Sopas',
            'description': 'Sopas tradicionales chinas',
            'icon': '🍲'
        },
        {
            'id': 'entradas',
            'name': 'Entradas',
            'description': 'Wantanes, enrollados y más',
            'icon': '🥟'
        },
        {
            'id': 'bebidas',
            'name': 'Bebidas',
            'description': 'Bebidas frías y calientes',
            'icon': '🥤'
        },
        {
            'id': 'postres',
            'name': 'Postres',
            'description': 'Postres tradicionales',
            'icon': '🍮'
        }
    ]
    
    return response(200, {
        'success': True,
        'count': len(categories),
        'data': categories
    })