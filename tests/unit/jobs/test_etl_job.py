"""
Unit tests for the ETLJob base module.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""

import asyncio
import logging

import pytest
from pytest import LogCaptureFixture

from src.jobs.etl_job import ETLJob


class MockETLJob(ETLJob):
    """Mock ETLJob for testing purposes."""

    def run(self):
        """Mock run method."""
        self.logger.info("Mock ETLJob run method executed.")

    async def async_run(self):
        """Mock async_run method."""
        self.logger.info("Mock ETLJob async_run method executed.")


def test_etl_job_run_method(caplog: LogCaptureFixture):
    """Test the run method of the ETLJob."""
    with caplog.at_level(logging.INFO):
        MockETLJob.execute()
    assert "Mock ETLJob run method executed." in caplog.text
    assert "ETL job completed successfully." in caplog.text


def test_etl_job_async_run_method(caplog: LogCaptureFixture):
    """Test the async_run method of the ETLJob."""
    with caplog.at_level(logging.INFO):
        MockETLJob.async_execute()
    assert "Mock ETLJob async_run method executed." in caplog.text
    assert "ETL job completed successfully." in caplog.text


def test_etl_job_run_method_exception(caplog: LogCaptureFixture):
    """Test the run method of the ETLJob with an exception."""

    class ExceptionETLJob(ETLJob):
        def run(self):
            raise ValueError("Test exception")

        async def async_run(self):
            pass

    with caplog.at_level(logging.ERROR):
        ExceptionETLJob.execute()
    assert "Error during ETL job: Test exception" in caplog.text


def test_etl_job_async_run_method_exception(caplog: LogCaptureFixture):
    """Test the async_run method of the ETLJob with an exception."""

    class ExceptionAsyncETLJob(ETLJob):
        async def async_run(self):
            raise ValueError("Test async exception")

        def run(self):
            pass

    with caplog.at_level(logging.ERROR):
        ExceptionAsyncETLJob.async_execute()
    assert "Error during ETL job: Test async exception" in caplog.text


def test_etl_job_not_implemented_run():
    """Test the ETLJob with a not implemented run method."""

    class DerivedETLJob(ETLJob):
        def run(self):
            super().run()

        async def async_run(self):
            pass

    with pytest.raises(NotImplementedError):
        DerivedETLJob().run()


def test_etl_job_not_implemented_async_run():
    """Test the ETLJob with a not implemented async_run method."""

    class DerivedETLJob(ETLJob):
        def run(self):
            pass

        async def async_run(self):
            await super().async_run()

    with pytest.raises(NotImplementedError):
        asyncio.run(DerivedETLJob().async_run())
