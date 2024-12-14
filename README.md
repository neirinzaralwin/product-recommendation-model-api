# Project Structure

```bash
ml_project/
├── data/
│   ├── raw/                # Raw, unprocessed data
│   ├── processed/          # Processed/cleaned data
│   └── README.md           # Data documentation
├── notebooks/
│   ├── eda.ipynb           # Exploratory Data Analysis
│   └── experiments.ipynb   # Experimenting with models
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── preprocess.py   # Data preprocessing scripts
│   │   └── load_data.py    # Scripts to load datasets
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py        # Model training logic
│   │   └── evaluate.py     # Model evaluation scripts
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py      # Utility functions
│   └── config.py           # Configuration variables
├── tests/
│   ├── __init__.py
│   ├── test_preprocess.py  # Unit tests for preprocessing
│   └── test_models.py      # Unit tests for models
├── scripts/
│   ├── run_training.py     # Script to run model training
│   ├── run_inference.py    # Script to make predictions
│   └── generate_report.py  # Script to create result reports
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
├── .gitignore              # Ignored files and directories
└── main.py
```

## Steps

```bash
source ./recom-fast-api/bin/activate
```

```bash
uvicorn --reload app.main:app
```
