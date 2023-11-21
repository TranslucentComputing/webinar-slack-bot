"""
ETL Job Base Module.

This module provides an abstract base class for defining ETL jobs. 
Each specific ETL job should extend this class and implement the required methods.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import asyncio
import logging
import sys
from abc import ABC, abstractmethod


class ETLJob(ABC):
    """
    Abstract base class for all ETL jobs.

    This class provides a standardized structure for defining and executing ETL jobs.
    Derived classes should implement the `run` or `async_run` method to provide specific ETL logic.

    Attributes:
        None

    Methods:
        run: Abstract method to be implemented by derived classes. Contains the ETL logic.
        async_run: Abstract asynchronous method to be implemented by derived classes.
            Contains the ETL logic.
        execute: Class method to instantiate and run the ETL job.
        async_execute: Class method to instantiate and run the ETL job asynchronously.
    """

    def __init__(self):
        """Initialize the ETLJob with a logger."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.configure_logger()

    def configure_logger(self):
        """Configure the logger."""
        self.logger.setLevel(logging.DEBUG)

        # Remove any existing handlers.
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Create new handler, targeting docker logs, sending to the console.
        handler = logging.StreamHandler(sys.stdout)

        # Set the formatter for the handler.
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    @abstractmethod
    def run(self) -> None:
        """
        Execute the ETL job.

        This abstract method should be implemented by derived classes to provide
        the specific ETL logic for the job.

        Raises:
            NotImplementedError: If the method is not implemented by the derived class.
        """
        raise NotImplementedError("The run method must be implemented by derived classes.")

    @abstractmethod
    async def async_run(self) -> None:
        """
        Execute the ETL job asynchronously.

        This abstract method should be implemented by derived classes to provide
        the specific ETL logic for the job.

        Raises:
            NotImplementedError: If the method is not implemented by the derived class.
        """
        raise NotImplementedError("The async_run method must be implemented by derived classes.")

    @classmethod
    def execute(cls) -> None:
        """
        Class method to instantiate and run the ETL job.

        This method creates an instance of the ETL job and then calls its `run` method.
        """
        job_instance = cls()
        try:
            job_instance.run()
            job_instance.logger.info("ETL job completed successfully.")
        except Exception as exc:
            job_instance.logger.exception("Error during ETL job: %s", str(exc))

    @classmethod
    def async_execute(cls) -> None:
        """
        Class method to instantiate and run the ETL job asynchronously.

        This method creates an instance of the ETL job and then calls its `async_run` method.
        """
        job_instance = cls()
        try:
            asyncio.run(job_instance.async_run())
            job_instance.logger.info("ETL job completed successfully.")
        except Exception as exc:
            job_instance.logger.exception("Error during ETL job: %s", str(exc))
