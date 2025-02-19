import time
from typing import Tuple

from opentelemetry import trace
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ASGIApp, Scope, Receive, Send

from .labels import (
    INFO,
    RESPONSES,
    REQUESTS_IN_PROGRESS,
    REQUESTS,
    REQUESTS_PROCESSING_TIME,
    EXCEPTIONS,
)


class PrometheusMiddleware:
    def __init__(self, app: ASGIApp, app_name: str = "FastAPI") -> None:
        self.app = app
        self.app_name = app_name
        INFO.labels(app_name=self.app_name).inc()

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        status_code = HTTP_500_INTERNAL_SERVER_ERROR
        method = request.method
        path, is_handled_path = self.get_path(request)

        if not is_handled_path:
            await self.app(scope, receive, send)
            return

        REQUESTS_IN_PROGRESS.labels(
            method=method, path=path, app_name=self.app_name
        ).inc()
        REQUESTS.labels(method=method, path=path, app_name=self.app_name).inc()
        before_time = time.perf_counter()
        try:
            response = Response()
            await self.app(scope, receive, response.send)
            status_code = response.status_code
        except BaseException as e:
            EXCEPTIONS.labels(
                method=method,
                path=path,
                exception_type=type(e).__name__,
                app_name=self.app_name,
            ).inc()
            raise e from None
        else:
            after_time = time.perf_counter()
            span = trace.get_current_span()
            trace_id = trace.format_trace_id(span.get_span_context().trace_id)

            REQUESTS_PROCESSING_TIME.labels(
                method=method, path=path, app_name=self.app_name
            ).observe(after_time - before_time, exemplar={"TraceID": trace_id})
        finally:
            RESPONSES.labels(
                method=method,
                path=path,
                status_code=status_code,
                app_name=self.app_name,
            ).inc()
            REQUESTS_IN_PROGRESS.labels(
                method=method, path=path, app_name=self.app_name
            ).dec()

    @staticmethod
    def get_path(request: Request) -> Tuple[str, bool]:
        for route in request.app.routes:
            match, child_scope = route.matches(request.scope)
            if match == Match.FULL:
                return route.path, True

        return request.url.path, False
