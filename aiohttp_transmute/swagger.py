import json
from aiohttp import web
from swagger_schema import Swagger, Info

from web_transmute.swagger import (
    generate_swagger,
    get_swagger_static_root
)

STATIC_ROOT = "/_swagger/static"


def add_swagger_api_route(app, target_route, swagger_json_route):
    """
    add the swagger statics to the route,
    """
    static_root = get_swagger_static_root()
    swagger_body = generate_swagger(STATIC_ROOT, swagger_json_route).encode("utf-8")

    async def swagger_ui(request):
        return web.Response(body=swagger_body)

    app.router.add_route("GET", target_route, swagger_ui)
    app.router.add_static(STATIC_ROOT, static_root)


def create_swagger_json_handler(app):

    spec = Swagger(
        info=Info(title="example", version="1.0"),
        paths=app.router.swagger_paths(),
        swagger="2.0",
    ).dump()
    encoded_spec = json.dumps(spec).encode("UTF-8")

    async def swagger(request):
        return web.Response(
            # we allow CORS, so this can be requested at swagger.io
            headers={
                "Access-Control-Allow-Origin": "*"
            },
            body=encoded_spec
        )

    return swagger
