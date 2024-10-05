import uvicorn
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator, metrics
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

instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/openapi.json", "/favicon.ico"],
    inprogress_name="in_progress",
    inprogress_labels=True,
)

TRACKED_METRICS = [
    metrics.requests(),
    metrics.latency(),
]

for metric in TRACKED_METRICS:
    instrumentator.add(metric)

instrumentator.instrument(app, metric_namespace="service", metric_subsystem="service")
instrumentator.expose(app, include_in_schema=False, should_gzip=True)


@app.exception_handler(Exception)
async def custom_exception_handler(_: Request, exception: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(exception)})


@app.on_event("startup")
async def initialize_db():
    await init_tables()


for router in all_routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
