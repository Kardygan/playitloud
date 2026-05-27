from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from playitloud.routers import addresses, albums, artists, users

app = FastAPI(title="Playitloud API")

app.include_router(users.router)
app.include_router(addresses.router)
app.include_router(artists.router)
app.include_router(albums.router)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    msg = str(exc)
    if "already exists" in msg:
        status_code = 409
    elif "not found" in msg.lower():
        status_code = 404
    else:
        status_code = 400
    return JSONResponse(status_code=status_code, content={"detail": msg})
