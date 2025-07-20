import os
from src import metric

def test_metrics_file_created():
    metric.calc_metrics()
    assert os.path.exists('results/metrics_report.md')
