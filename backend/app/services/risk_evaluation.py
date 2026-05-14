import os
import asyncio
import logging
from typing import Any, Dict

from app.uniqueness import uniqueness_and_rare_combination
from app.linkage import linkage_reidentification_risk

logger = logging.getLogger(__name__)


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

    This function currently runs:
    1. Uniqueness and rare-combination risk
    2. Linkage / re-identification risk

    Args:
        real_uuid: UUID of the real dataset file.
        synthetic_uuid: UUID of the synthetic dataset file.
        qi_list: List of quasi-identifiers.
        sa_list: List of sensitive attributes.
        real_path: File path of the uploaded real dataset.
        synthetic_path: File path of the uploaded synthetic dataset.

    Returns:
        Dictionary containing risk evaluation results and generated file paths.
    """

    result_dir = os.path.join("results", f"{real_uuid}_{synthetic_uuid}")
    logger.info(
        "Creating result directory for risk evaluation: %s",
        result_dir,
    )
    os.makedirs(result_dir, exist_ok=True)

    # uniqueness and rare-combination output files.
    out_csv = os.path.join(result_dir, "syn_flags.csv")
    out_full_csv = os.path.join(result_dir, "syn_per_record.csv")
    out_json = os.path.join(result_dir, "syn_k_summary.json")
    out_qid_stats_csv = os.path.join(result_dir, "qid_group_stats.csv")

    # linkage / re-identification output files.
    linkage_per_record_csv = os.path.join(result_dir, "linkage_per_record.csv")
    linkage_summary_json = os.path.join(result_dir, "linkage_summary.json")

    # uniqueness risk evaluation 
    logger.info(
        "Starting uniqueness evaluation for real_path=%s synthetic_path=%s",
        real_path,
        synthetic_path,
    )
    uniqueness_result = await asyncio.to_thread(
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
    logger.info(
        "Uniqueness evaluation complete. outputs=%s, %s, %s, %s",
        out_csv,
        out_full_csv,
        out_json,
        out_qid_stats_csv,
    )

    # linkage / re-identification risk evaluation
    logger.info(
        "Starting linkage risk evaluation for real_path=%s synthetic_path=%s qis=%s",
        real_path,
        synthetic_path,
        qi_list,
    )
    linkage_result = await asyncio.to_thread(
        linkage_reidentification_risk,
        real_path=real_path,
        synthetic_path=synthetic_path,
        qis=qi_list,
        out_per_record_csv=linkage_per_record_csv,
        out_json=linkage_summary_json,
    )
    logger.info(
        "Linkage evaluation complete. outputs=%s, %s",
        linkage_per_record_csv,
        linkage_summary_json,
    )

    return {
        "real_uuid": real_uuid,
        "synthetic_uuid": synthetic_uuid,
        "qi_list": qi_list,
        "sa_list": sa_list,
        "result_dir": result_dir,
        "files": {
            # uniqueness files.
            "syn_flags": out_csv,
            "syn_per_record": out_full_csv,
            "summary_json": out_json,
            "qid_group_stats": out_qid_stats_csv,

            # linkage files.
            "linkage_per_record": linkage_per_record_csv,
            "linkage_summary": linkage_summary_json,
        },
        "summary": {
            "uniqueness_and_rare_combination": uniqueness_result,
            "linkage_reidentification": linkage_result,
        },
    }