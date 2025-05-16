
import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import db, Producto

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:////app/db.sqlite3'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
       pass
   
    @app.route('/api/productos-stock/', methods=['GET'])
    def productos_stock():
        productos = Producto.query.filter(Producto.stock > 0).all()
        resultado = []
        base_media = os.getenv('MEDIA_BASE_URL', 'http://localhost:8000/media/')
        for p in productos:
            resultado.append({
                'id': p.id,
                'titulo': p.titulo,
                'descripcion': p.descripcion,
                'precio': str(p.precio),
                'stock': p.stock,
                'categoria_id': p.categoria_id,
                'imagen_url': p.imagen and f"{base_media}{p.imagen}",
            })
        return jsonify({'productos': resultado})
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
