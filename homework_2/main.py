import uvicorn
from fastapi import FastAPI, Request
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from homework_2.infrastructure.controllers.routers import all_routers
from homework_2.infrastructure.db.utils import init_tables

app = FastAPI(title="Shop API", swagger_ui_parameters={"defaultModelsExpandDepth": -1})
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def custom_exception_handler(_: Request, exception: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(exception)})


@app.on_event("startup")
async def initialize_db():
    await init_tables()


for router in all_routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
