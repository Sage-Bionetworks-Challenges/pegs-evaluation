# PEGS Evaluation
Validation and scoring scripts for Task 1 of the [PEGS Challenge](https://www.synapse.org/pegs).

Metrics returned and used for ranking are:

* Primary: area under the receiver operating characteristic curve (AUROC)

* Secondary (used for ties): area under the precision-recall curve (AUPRC)

## 🐍 Using Python

### Validate

```text
python validate.py \
  -p PATH/TO/PREDICTIONS_FILE.CSV \
  -g PATH/TO/GOLDSTANDARD_FILE.CSV [-o RESULTS_FILE]
```
If `-o/--output` is not provided, then results will print to STDOUT, e.g.

```json
{"validation_status": "VALIDATED", "validation_errors": ""}
```

What it will check for:

* two columns named `id` and `disease_probability` (extraneous columns will be ignored)
* `id` values are strings
* `disease_probability` values are floats between 0.0 and 1.0, and cannot be null/None
* there is one prediction per patient (so, no missing patient IDs or duplicate patient IDs)
* there are no extra predictions (so, no unknown patient IDs)

### Score

```text
python score.py \
  -p PATH/TO/PREDICTIONS_FILE.CSV \
  -g PATH/TO/GOLDSTANDARD_FILE.CSV [-o RESULTS_FILE]
```

If `-o/--output` is not provided, then results will output to `results.json`.

## 🐳 Using Docker 

Results will be outputted to `output/results.json` in your current working directory (assuming you mount `$PWD/output`).

### Validate

```
docker run --rm \
  -v /PATH/TO/PREDICTIONS_FILE.CSV:/predictions.csv:ro \
  -v /PATH/TO/GOLDSTANDARD_FILE.CSV:/goldstandard.csv:ro \
  -v $PWD/output:/output:rw \
  ghcr.io/sage-bionetworks-challenges/pegs-evaluation:v1.0.0 \
  validate.py \
  -p /predictions.csv -g /goldstandard.csv -o /output/results.json
```

### Score

```
docker run --rm \
  -v /PATH/TO/PREDICTIONS_FILE.CSV:/predictions.csv:ro \
  -v /PATH/TO/GOLDSTANDARD_FILE.CSV:/goldstandard.csv:ro \
  -v $PWD/output:/output:rw \
  ghcr.io/sage-bionetworks-challenges/pegs-evaluation:v1.0.0 \
  validate.py \
  -p /predictions.csv -g /goldstandard.csv -o /output/results.json
```
