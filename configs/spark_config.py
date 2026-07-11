"""Spark session configuration helpers."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class SparkConfig:
    """Settings for building Spark sessions."""

    app_name: str = os.getenv("SPARK_APP_NAME", "bitestream")
    master: str = os.getenv("SPARK_MASTER", "local[*]")
    shuffle_partitions: str = os.getenv("SPARK_SHUFFLE_PARTITIONS", "8")

    def as_dict(self) -> dict:
        """Return Spark configs suitable for ``SparkSession.builder.config``."""
        return {
            "spark.sql.shuffle.partitions": self.shuffle_partitions,
        }


spark_config = SparkConfig()


def build_spark_session():
    """Create and return a configured SparkSession.

    Imported lazily so the module is usable without PySpark installed.
    """
    from pyspark.sql import SparkSession  # noqa: WPS433 (local import by design)

    builder = SparkSession.builder.appName(spark_config.app_name).master(spark_config.master)
    for key, value in spark_config.as_dict().items():
        builder = builder.config(key, value)
    return builder.getOrCreate()
