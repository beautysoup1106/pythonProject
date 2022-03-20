
import uvicorn
from fastapi import FastAPI
from starlette.responses import Response

from routers.items import itemRoute
from routers.users import userRoute

app = FastAPI(
    docs_url="/openapi",
    redoc_url="/apidoc"
)

app.include_router(userRoute, prefix="/user", tags=["users"])
app.include_router(itemRoute, prefix="/items", tags=["items"])


@app.get("/legacy/")
def get_legacy_data(response: Response):
    headers = {"X-Cat": "yxxtest", "Content_Language": "en-US"}
    data = """
    <?xml version="1.0?>
    <shampoo>
    <Header>
    Apply shampoo here
    </Header>
    <Body>
        You will have to use soup here

    </Body>
    </shampoo>
    """

    response.set_cookie(key="message", value="hello")
    return Response(content=data, media_type="application/xml", headers=headers)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8020)
