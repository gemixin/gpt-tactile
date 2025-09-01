# GPT-Tactile

## Overview

**GPT-Tactile** is a collection of scripts for visuo-tactile object exploration and classification using a [DIGIT](https://digit.ml/) tactile sensor and the [OpenAI API](https://platform.openai.com/docs/overview). The project is designed to:

- Allow GPT to interactively instruct a human to probe objects with a DIGIT sensor, collect tactile images, and iteratively refine object predictions.
- Evaluate both open-ended and multi-choice prompt strategies.
- Assess GPT's ability to classify objects from tactile data, both in static (batch) and interactive (exploratory) settings.

## Requirements

- **Operating System:** Linux only (DIGIT sensors are supported on Linux only)
- **Tested Environment:** Ubuntu 22.04, Python 3.13.5
- **Python Environment:** Regular Python or Anaconda environment
- **Packages:** [digit-interface](https://github.com/facebookresearch/digit-interface), [openai](https://github.com/openai/openai-python)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/gemixin/gpt-tactile.git
cd gpt-tactile
```

### 2. Install dependencies

#### Option A: With pip

1. *(Optional)* Set up a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

#### Option B: With Anaconda

Create a new conda environment using the provided `environment.yml`:

```bash
conda env create -f environment.yml
conda activate gpt-tactile
```

## OpenAI API Setup

You will need your own API key, exported as an environment variable. See the [official documentation](https://platform.openai.com/docs/libraries) for details.

## Running the Scripts

### Static Classification

The script sends GPT a collection of 6 previously collected tactile images for five different objects (see `static/images/`). It does this for both prompt types (multi-choice and open-ended). 
It stores the classification predictions in the `static` folder.
```bash
python3 static_classification.py
```

### Simple Active Exploration

Interactive script where GPT guides the user to move the DIGIT sensor and capture images, aiming to classify the object.
It stores the conversation history and captured tactile images in the `simple_active` folder.
```bash
python3 simple_active_exploration.py
```

### Active Exploration

Similar to simple active, but with more explicit movement/rotation commands and axis-based control.
It stores the conversation history and captured tactile images in the `active` folder.
```bash
python3 active_exploration.py
```

## Prompts

The prompts for each experiment type (static, active, simple active) can be found in their respective `initial` folders.

## Results

Results from my own experiments have been manually saved in the `results` folders.

## Analysis

As expected, GPT models currently struggle to interpret tactile images. During active exploration, the model struggled to understand the spatial properties of objects and often produced incorrect classifications. Performance on static images was similarly poor. These results underscore the need for pre-training on tactile data and the development of more advanced models.

## Citation

If you use DIGIT or this repo in your research, please cite:

**DIGIT: A Novel Design for a Low-Cost Compact High-Resolution Tactile Sensor with Application to In-Hand Manipulation**  
Mike Lambeta, Po-Wei Chou, Stephen Tian, Brian Yang, Benjamin Maloon, Victoria Rose Most, Dave Stroud, Raymond Santos, Ahmad Byagowi, Gregg Kammerer, Dinesh Jayaraman, Roberto Calandra  
_IEEE Robotics and Automation Letters (RA-L), vol. 5, no. 3, pp. 3838–3845, 2020_  
[https://doi.org/10.1109/LRA.2020.2977257](https://doi.org/10.1109/LRA.2020.2977257)