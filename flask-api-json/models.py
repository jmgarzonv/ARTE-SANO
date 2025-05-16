from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    __tablename__ = 'app_producto'
    id          = db.Column(db.Integer, primary_key=True)
    titulo      = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio      = db.Column(db.Numeric(10,2), nullable=False)
    stock       = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(500), nullable=True)