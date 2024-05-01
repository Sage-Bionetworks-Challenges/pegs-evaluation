#!/usr/bin/env python3
"""Score prediction file for Task 1.

Metrics to return:
    - ROC curve
    - PR curve
"""

import argparse
import json

import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score


def get_args():
    """Set up command-line interface and get arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--predictions_file", type=str, required=True)
    parser.add_argument("-g", "--goldstandard_file", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, default="results.json")
    return parser.parse_args()


def score(gold, gold_col, pred, pred_col):
    """
    Calculate metrics for: AUC-ROC, AUCPR
    """
    roc = roc_auc_score(gold[gold_col], pred[pred_col])
    pr = average_precision_score(gold[gold_col], pred[pred_col])

    return {"auc_roc": roc, "auprc": pr}


def main():
    """Main function."""
    args = get_args()

    with open(args.output, encoding="utf-8") as out:
        res = json.load(out)

    if res.get("validation_status") == "VALIDATED":
        pred = pd.read_csv(args.predictions_file)
        gold = pd.read_csv(args.goldstandard_file)
        scores = score(gold, "disease", pred, "disease_probability")
        status = "SCORED"
    else:
        scores = {"auc_roc": None, "auprc": None}
        status = "INVALID"

    res |= {
        "score_status": status,
        "score_errors": (
            ""
            if status == "SCORED"
            else "Prediction file invalid; cannot be scored."
        ),
        ** scores
    }
    with open(args.output, "w", encoding="utf-8") as out:
        out.write(json.dumps(res))


if __name__ == "__main__":
    main()
