from main import app
from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi

asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app, lifespan="off")
