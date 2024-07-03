#!/usr/bin/env python3
"""Score prediction file for Task 1.

Metrics to return:
    - ROC curve
    - PR curve
"""
from glob import glob
import argparse
import json
import os

import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score

GOLDSTANDARD_COLS = {"epr_number": str, "disease_probability": str}
PREDICTION_COLS = {"epr_number": str, "disease_probability": np.float64}


def get_args():
    """Set up command-line interface and get arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--predictions_file", type=str, required=True)
    parser.add_argument("-g", "--goldstandard_folder", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, default="results.json")
    return parser.parse_args()


def score(gold, pred, id_colname, prob_colname):
    """
    Calculate metrics for: AUC-ROC, AUCPR
    """
    # Join the two dataframes so that the order of the ids are the same
    # between goldstandard and prediction.
    merged = gold.merge(pred, how="left", on=id_colname)
    roc = roc_auc_score(
        merged[prob_colname + "_x"],
        merged[prob_colname + "_y"]
    )
    pr = average_precision_score(
        merged[prob_colname + "_x"],
        merged[prob_colname + "_y"]
    )
    return {"auc_roc": roc, "auprc": pr}


def extract_gs_file(folder):
    """Extract gold standard file from folder."""
    files = glob(os.path.join(folder, "*"))
    if len(files) != 1:
        raise ValueError(
            "Expected exactly one gold standard file in folder. "
            f"Got {len(files)}. Exiting."
        )

    return files[0]


def preprocess(df, colname):
    """Preprocess dataframe and convert column as needed."""
    df = df[~df[colname].isin([".M"])]
    df[colname] = df[colname].astype(int)
    return df


def main():
    """Main function."""
    args = get_args()

    with open(args.output, encoding="utf-8") as out:
        res = json.load(out)

    gold_file = extract_gs_file(args.goldstandard_folder)

    scores = {"auc_roc": None, "auprc": None}
    status = "INVALID"
    if res.get("validation_status") == "VALIDATED":
        try:
            pred = pd.read_csv(
                args.predictions_file,
                usecols=PREDICTION_COLS,
                dtype=PREDICTION_COLS
            )
            gold = pd.read_csv(
                gold_file,
                usecols=GOLDSTANDARD_COLS,
                dtype=GOLDSTANDARD_COLS
            )
            gold = preprocess(gold, "disease_probability")
            scores = score(gold, pred, "epr_number", "disease_probability")
            status = "SCORED"
            errors = ""
        except ValueError:
            errors = "An error was encountered during scoring; submission not evaluated."
    else:
        errors = "Submission could not be evaluated due to validation errors."

    res |= {
        "score_status": status,
        "score_errors": errors,
        **scores,
    }
    with open(args.output, "w", encoding="utf-8") as out:
        out.write(json.dumps(res))
    print(status)


if __name__ == "__main__":
    main()
