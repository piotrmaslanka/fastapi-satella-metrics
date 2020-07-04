
fastapi-satella-metrics
=======================

[![Build Status](https://travis-ci.com/piotrmaslanka/fastapi-satella-metrics.svg?branch=master)](https://travis-ci.com/piotrmaslanka/fastapi-satella-metrics)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7ee3acc2a4ede5903517/test_coverage)](https://codeclimate.com/github/piotrmaslanka/fastapi-satella-metrics/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/7ee3acc2a4ede5903517/maintainability)](https://codeclimate.com/github/piotrmaslanka/fastapi-satella-metrics/maintainability)
[![Issue Count](https://codeclimate.com/github/piotrmaslanka/fastapi-satella-metrics/badges/issue_count.svg)](https://codeclimate.com/github/piotrmaslanka/fastapi-satella-metrics)
[![PyPI](https://img.shields.io/pypi/pyversions/fastapi-satella-metrics.svg)](https://pypi.python.org/pypi/fastapi-satella-metrics)
[![PyPI version](https://badge.fury.io/py/fastapi-satella-metrics.svg)](https://badge.fury.io/py/fastapi-satella-metrics)
[![PyPI](https://img.shields.io/pypi/implementation/fastapi-satella-metrics.svg)](https://pypi.python.org/pypi/fastapi-satella-metrics)

fastapi-satella-metrics is an application to seamlessly measure your FastAPI
application using Satella's metrics.

# Installation
```bash
pip install fastapi-satella-metrics
```

# Example use

## Collecting metrics

```python
import fastapi
from fastapi_satella_metrics import SatellaMetricsMiddleware

app = fastapi.FastAPI()
SatellaMetricsMiddleware(app)
```

## Exporting metrics for Prometheus

Using an external thread:

```python
from satella.instrumentation.metrics.exporters import PrometheusHTTPExporterThread

phet = PrometheusHTTPExporterThread('0.0.0.0', 8080, {'extra_label_1': 'extra_value'})
phet.start()
```

Or, if you desire to export your metrics within FastAPI, just use:

```python
import fastapi
from fastapi_satella_metrics import PrometheusExporter

app = fastapi.FastAPI()
PrometheusExporter(app, {'extra_label_1': 'extra_value'})
```
