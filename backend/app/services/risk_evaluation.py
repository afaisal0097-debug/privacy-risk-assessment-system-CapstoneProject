import os
import asyncio
from typing import Any, Dict

from app.uniqueness import uniqueness_and_rare_combination


async def risk_evaluation(
    real_uuid: str,
    synthetic_uuid: str,
    qi_list: list[str],
    sa_list: list[str],
    real_path: str,
    synthetic_path: str,
) -> Dict[str, Any]:
    """
    Performs privacy risk evaluation on uploaded real and synthetic datasets.

    Args:
        real_uuid: UUID of the real dataset file.
        synthetic_uuid: UUID of the synthetic dataset file.
        qi_list: List of quasi-identifiers.
        sa_list: List of sensitive attributes.
        real_path: File path of the uploaded real dataset.
        synthetic_path: File path of the uploaded synthetic dataset.

    Returns:
        Dictionary containing uniqueness and rare-combination results.
    """

    result_dir = os.path.join("results", f"{real_uuid}_{synthetic_uuid}")
    os.makedirs(result_dir, exist_ok=True)

    out_csv = os.path.join(result_dir, "syn_flags.csv")
    out_full_csv = os.path.join(result_dir, "syn_per_record.csv")
    out_json = os.path.join(result_dir, "syn_k_summary.json")
    out_qid_stats_csv = os.path.join(result_dir, "qid_group_stats.csv")

    result = await asyncio.to_thread(
        uniqueness_and_rare_combination,
        real_path=real_path,
        synthetic_path=synthetic_path,
        qis=qi_list,
        sas=sa_list,
        out_csv=out_csv,
        out_full_csv=out_full_csv,
        out_json=out_json,
        out_qid_stats_csv=out_qid_stats_csv,
    )

    return {
        "real_uuid": real_uuid,
        "synthetic_uuid": synthetic_uuid,
        "qi_list": qi_list,
        "sa_list": sa_list,
        "result_dir": result_dir,
        "files": {
            "syn_flags": out_csv,
            "syn_per_record": out_full_csv,
            "summary_json": out_json,
            "qid_group_stats": out_qid_stats_csv,
        },
        "summary": result,
    }