from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics

from homework_4.api import users, utils


def create_app():
    app = FastAPI(
        title="Testing Demo Service",
        lifespan=utils.initialize,
    )

    app.add_exception_handler(ValueError, utils.value_error_handler)
    app.include_router(users.router)

    return app


app = create_app()
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
