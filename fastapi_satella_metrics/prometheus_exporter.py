import typing as tp

import fastapi
from satella.instrumentation.metrics import getMetric
from satella.instrumentation.metrics.exporters import metric_data_collection_to_prometheus


def PrometheusExporter(app: fastapi.FastAPI,
                       extra_labels: tp.Optional[dict] = None,
                       url: str = '/metrics') -> None:
    labels = extra_labels or {}

    @app.get(url)
    def export_prometheus():
        metric = getMetric()
        metric_data = metric.to_metric_data()
        new_values = set()
        for datum in metric_data.values:
            if not datum.internal:
                new_values.add(datum)
        metric_data.values = new_values
        metric_data.add_labels(labels)
        return fastapi.Response(content=metric_data_collection_to_prometheus(metric_data),
                                media_type='text/plain')


