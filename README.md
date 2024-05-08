# PEGS Evaluation
Validation and scoring scripts for Task 1 of the [PEGS Challenge](https://www.synapse.org/pegs).
For Task 2, see `writeup-workflow/`.

Metrics returned and used for ranking are:

* Primary: area under the receiver operating characteristic curve (AUROC)

* Secondary (used for ties): area under the precision-recall curve (AUPRC)

## 🐍 Using Python

### Validate

```text
python validate.py \
  -p PATH/TO/PREDICTIONS_FILE.CSV \
  -g PATH/TO/GOLDSTANDARD_FOLDER [-o RESULTS_FILE]
```

If `-o/--output` is not provided, then full results will output to `results.json`.

What it will check for:

* two columns named `id` and `disease_probability` (extraneous columns will be ignored)
* `id` values are strings
* `disease_probability` values are floats between 0.0 and 1.0, and cannot be null/None
* there is one prediction per patient (so, no missing patient IDs or duplicate patient IDs)
* there are no extra predictions (so, no unknown patient IDs)

The script will either print to STDOUT, `VALIDATED` or `INVALID`.

### Score

```text
python score.py \
  -p PATH/TO/PREDICTIONS_FILE.CSV \
  -g PATH/TO/GOLDSTANDARD_FOLDER [-o RESULTS_FILE]
```

If `-o/--output` is not provided, then results will output to `results.json`.

The script will either print to STDOUT, `SCORED` or `INVALID`.

## 🐳 Using Docker 

Results will be outputted to `output/results.json` in your current working directory (assuming you mount `$PWD/output`).

### Validate

```
docker run --rm \
  -v /PATH/TO/PREDICTIONS_FILE.CSV:/predictions.csv:ro \
  -v /PATH/TO/GOLDSTANDARD_FOLDER:/goldstandard:ro \
  -v $PWD/output:/output:rw \
  ghcr.io/sage-bionetworks-challenges/pegs-evaluation:latest \
  python3 validate.py \
  -p /predictions.csv -g /goldstandard -o /output/results.json
```

### Score

```
docker run --rm \
  -v /PATH/TO/PREDICTIONS_FILE.CSV:/predictions.csv:ro \
  -v /PATH/TO/GOLDSTANDARD_FOLDER:/goldstandard:ro \
  -v $PWD/output:/output:rw \
  ghcr.io/sage-bionetworks-challenges/pegs-evaluation:latest \
  python3 score.py \
  -p /predictions.csv -g /goldstandard -o /output/results.json
```
