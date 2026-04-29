"""Validation constants used across the backend app.

This module centralises the default quasi-identifiers (QIs) and
sensitive attributes (SAs) so other modules can import them.
"""
from __future__ import annotations

DEFAULT_QIS = [
    "age",
    "gender",
    "race",
    "admission_type_id",
    "discharge_disposition_id",
    "time_in_hospital",
]

DEFAULT_SAS = ["diag_1", "num_medications", "num_lab_procedures"]
