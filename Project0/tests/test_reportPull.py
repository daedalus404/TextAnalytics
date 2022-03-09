import pytest
import project0

def test_pull():
    pullReportPdf("https://www.normanok.gov/sites/default/files/documents/2022-03/2022-03-01_daily_incident_summary.pdf")
    assert os.path.exists("temp/2022-03-01_daily_incident_summary.pdf")