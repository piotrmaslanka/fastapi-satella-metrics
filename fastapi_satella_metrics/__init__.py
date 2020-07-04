import typing as tp

import fastapi

from satella.time import measure
from satella.instrumentation.metrics import getMetric, Metric
from .prometheus_exporter import PrometheusExporter

__version__ = '1.0.2'

__all__ = ['SatellaMetricsMiddleware', 'PrometheusExporter', '__version__']


def SatellaMetricsMiddleware(app: fastapi.FastAPI, summary_metric: tp.Optional[Metric] = None,
                             histogram_metric: tp.Optional[Metric] = None,
                             response_codes_metric: tp.Optional[Metric] = None):
    """
    Install handlers to measure metrics on an application

    :param app: fastapi application to monitor
    :param summary_metric: summary metric to use. Should be of type 'summary'
    :param histogram_metric: histogram metric to use. Should be of type 'histogram'
    :param response_codes_metric: Response codes counter to use. Should be of type 'counter'
    """
    summary_metric = summary_metric or getMetric('requests_summary', 'summary',
                                    quantiles=[0.2, 0.5, 0.9, 0.95, 0.99])
    histogram_metric = histogram_metric or getMetric('requests_histogram', 'histogram')
    response_codes_metric = response_codes_metric or getMetric('requests_response_codes', 'counter')

    @app.middleware('http')
    async def do_middleware(request: fastapi.Request, call_next):
        with measure() as measurement:
            response = await call_next(request)

        summary_metric.runtime(measurement(), endpoint=str(request.url))
        histogram_metric.runtime(measurement(), endpoint=str(request.url))
        response_codes_metric.runtime(+1, response_code=response.status_code)
        return response
