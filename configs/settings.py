"""Central application settings loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass, field


def _get(key: str, default: str = "") -> str:
    return os.getenv(key, default)


@dataclass
class Settings:
    """Global project settings."""

    environment: str = field(default_factory=lambda: _get("ENVIRONMENT", "development"))
    log_level: str = field(default_factory=lambda: _get("LOG_LEVEL", "INFO"))

    # Data lake paths
    data_root: str = field(default_factory=lambda: _get("DATA_ROOT", "data"))

    # Warehouse
    gcp_project: str = field(default_factory=lambda: _get("GCP_PROJECT", ""))
    bigquery_dataset: str = field(default_factory=lambda: _get("BIGQUERY_DATASET", "bitestream"))

    @property
    def bronze_path(self) -> str:
        """Relative path to the bronze data lake layer."""
        return f"{self.data_root}/bronze"

    @property
    def silver_path(self) -> str:
        """Relative path to the silver data lake layer."""
        return f"{self.data_root}/silver"

    @property
    def gold_path(self) -> str:
        """Relative path to the gold data lake layer."""
        return f"{self.data_root}/gold"


settings = Settings()
