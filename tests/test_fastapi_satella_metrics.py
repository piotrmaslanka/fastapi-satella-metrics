import multiprocessing
import time
import unittest
import uvicorn
import logging
import atexit
import os
import signal

import fastapi
import requests
import coverage

import fastapi_satella_metrics

logger = logging.getLogger(__name__)
app = fastapi.FastAPI()
fastapi_satella_metrics.PrometheusExporter(app, {'service_name': 'my_service'})
fastapi_satella_metrics.SatellaMetricsMiddleware(app)


@app.get('/')
def endpoint():
    return ''


def start():
    coverage.process_startup()
    atexit.register(lambda: logger.warning('Finishing the server'))
    uvicorn.run('tests.test_fastapi_satella_metrics:app',
                host="127.0.0.1",
                port=8000,
                reload=True)


class TestFlaskSatellaMetrics(unittest.TestCase):
    def setUp(self) -> None:
        self.process = multiprocessing.Process(target=start)
        self.process.start()
        time.sleep(1)

    def tearDown(self) -> None:
        os.kill(self.process.pid, signal.SIGINT)
        self.process.join()

    def test_satella_metrics(self):
        q = requests.get('http://127.0.0.1:8000/')
        self.assertEqual(q.status_code, 200)

        q = requests.get('http://127.0.0.1:8000/metrics')
        self.assertEqual(q.status_code, 200)
        self.assertIn('service_name="my_service"', q.text)
        self.assertIn('requests_response_codes', q.text)
