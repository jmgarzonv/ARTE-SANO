# ARTE-SANO
##  Cómo ejecutar el proyecto

## 1. Clonar el repositorio
```bash
git clone https://github.com/jmgarzonv/ARTE-SANO.git
```

## 2. Cambiar a la rama login.
```bash
git checkout login
cd  ARTE-SANO-login
```
## 3. Instalar dependencias.
```bash
pip install -r requirements.txt

```
## Configurar la base de datos:
```bash
python manage.py migrate


```
## Ejecutar el servidor.
```bash
python manage.py runserver




```
## Finalmente abre el navegador con http://127.0.0.1:8000/


