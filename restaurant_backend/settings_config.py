from decouple import config

DEBUG_ = config("DEBUG", cast=bool, default=True)
SECRET_KEY_ = config("SECRET_KEY")


CONFIG_DEBUG = DEBUG_
CONFIG_SECRET_KEY = SECRET_KEY_

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default=f"http://localhost:{config('NGINX_EXPOSE_PORT')}, http://localhost:{config('BACKEND_EXPOSE_PORT')}",
)
