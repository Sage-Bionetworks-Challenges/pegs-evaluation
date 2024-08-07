#!/usr/bin/env python3
"""Validate prediction file for Task 1.

Prediction file should be a 2-column CSV file, where:
    - `id` is a string
    - `disease_probability` is a float between 0 and 1
"""
from glob import glob
import argparse
import json
import os

import numpy as np
import pandas as pd

GOLDSTANDARD_COLS = {"epr_number": str, "disease_probability": str}
EXPECTED_COLS = {"epr_number": str, "disease_probability": np.float64}


def get_args():
    """Set up command-line interface and get arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--predictions_file", type=str, required=True)
    parser.add_argument("-g", "--goldstandard_folder", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, default="results.json")
    return parser.parse_args()


def check_dups(pred):
    """Check for duplicate participant IDs."""
    duplicates = pred.duplicated(subset=["epr_number"])
    if duplicates.any():
        return (
            f"Found {duplicates.sum()} duplicate ID(s): "
            f"{pred[duplicates].epr_number.to_list()}"
        )
    return ""


def check_missing_ids(gold, pred):
    """Check for missing participant IDs."""
    pred = pred.set_index("epr_number")
    missing_ids = gold.index.difference(pred.index)
    if missing_ids.any():
        return (
            f"Found {missing_ids.shape[0]} missing ID(s): "
            f"{missing_ids.to_list()}"
        )
    return ""


def check_unknown_ids(gold, pred):
    """Check for unknown participant IDs."""
    pred = pred.set_index("epr_number")
    unknown_ids = pred.index.difference(gold.index)
    if unknown_ids.any():
        return (
            f"Found {unknown_ids.shape[0]} unknown ID(s): "
            f"{unknown_ids.to_list()}"
        )
    return ""


def check_nan_values(pred):
    """Check for NAN predictions."""
    missing_probs = pred["disease_probability"].isna().sum()
    if missing_probs:
        return f"'disease_probability' column contains {missing_probs} NaN value(s)."
    return ""


def check_prob_values(pred):
    """Check that probabilities are between [0, 1]."""
    if (pred["disease_probability"] < 0).any() or \
       (pred["disease_probability"] > 1).any():
        return "'disease_probability' values should be between [0, 1]."
    return ""


def extract_gs_file(folder):
    """Extract goldstandard file from folder."""
    files = glob(os.path.join(folder, "*"))
    if len(files) != 1:
        raise ValueError(
            "Expected exactly one goldstandard file in folder. "
            f"Got {len(files)}. Exiting."
        )
    return files[0]


def validate(gold_folder, pred_file):
    """Validate predictions file against goldstandard."""
    errors = []
    gold_file = extract_gs_file(gold_folder)
    gold = pd.read_csv(gold_file, dtype=GOLDSTANDARD_COLS, index_col="epr_number")
    try:
        pred = pd.read_csv(
            pred_file,
            usecols=EXPECTED_COLS,
            dtype=EXPECTED_COLS,
            float_precision="round_trip",
        )
    except ValueError as err:
        errors.append(
            f"Invalid column names and/or types: {str(err)}. "
            f"Expecting: {str(EXPECTED_COLS)}."
        )
    else:
        errors.append(check_dups(pred))
        errors.append(check_missing_ids(gold, pred))
        errors.append(check_unknown_ids(gold, pred))
        errors.append(check_nan_values(pred))
        errors.append(check_prob_values(pred))
    return errors


def main():
    """Main function."""
    args = get_args()

    if "INVALID" in args.predictions_file:
        with open(args.predictions_file, encoding="utf-8") as f:
            errors = [f.read()]
    else:
        errors = validate(
            gold_folder=args.goldstandard_folder,
            pred_file=args.predictions_file
        )

    invalid_reasons = "\n".join(filter(None, errors))
    status = "INVALID" if invalid_reasons else "VALIDATED"

    # truncate validation errors if >500 (character limit for sending email)
    if len(invalid_reasons) > 500:
        invalid_reasons = invalid_reasons[:496] + "..."
    res = json.dumps(
        {"validation_status": status, "validation_errors": invalid_reasons}
    )

    with open(args.output, "w") as out:
        out.write(res)
    print(status)


if __name__ == "__main__":
    main()
