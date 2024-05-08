"""Dummy model for PEGS"""

import os

import typer
import pandas as pd
import numpy as np


def predict(df):
    """
    Run a "prediction": generate random floats between [0.0, 1.0)
    """
    nrows = len(df.index)
    df["disease_probability"] = np.random.random_sample(size=nrows)
    return df


def main(input_dir: str = '/input',
         output_dir: str = "/output"):
    """
    Create a CLI with two args: `input_dir`, `output_dir`
    """
    data = pd.read_csv("ids.csv")
    predictions = predict(data)
    predictions.to_csv(os.path.join(output_dir, "predictions.csv"),
                       index=False)


if __name__ == "__main__":
    typer.run(main)
