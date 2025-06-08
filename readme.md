# Tiktok Engagement & Addiction Analysis

> "Emotional Engagement and TikTok Usage in Young Adults: A Multimodal Experimental Study"


## Table of contents

1. [Overview](#overview)
2. [Features](#features)
3. [Dataset](#dataset)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Analysis Methods](#analysis-methods)
7. [Results](#results)
8. [Visualization](#visualization)
9. [Contact](#contact)

---

## Overview
Excessive use of short-form video platforms like TikTok has raised concerns about digital addiction and its impact on young users’ emotional states. The objective is to investigate the correlation between continuous time spent on TikTok and emotional engagement in users aged 20–23. We collected multimodal data using the iMotions platform, integrating galvanic skin response (GSR) sensors and facial expression analysis via Affectiva’s AFFDEX SDK 5.1.

We binarized engagement using a logistc transformation and conducted a binomial test which showed engagement proportions significantly above a previously defined baseline. We also computed per-participant Pearson correlations between timestamp and normalized engagement which led to a negative correlation, indicating engagement tended to decrease over time. FInally GSR analysis revealed no significant increase in skin conductance during engaged vs no engaged moments.

---

## Features

- Real-time GSR data capture and processing
- Automated facial-expression recognition
- Time-series feature extraction (peaks, latencies, averages)
- Correlation analysis between physiological responses and time
- Configurable algorithm for high-intensity periods

---

## Dataset

- **Raw data:**
    - `participant_files/<ID>.csv`

- **Preprocessing steps:**
    - Timestamp alignment
    - Missing-value imputation
    - Baseline normalization

---

## Prerquisites
Before using this repository, you must have:

1. **iMotions®** platform installed and licensed  
   – Includes Galvanic Skin Response (GSR) sensor support.  
2. **Affectiva AFFDEX SDK 5.1**  
   – Ensure you have a valid license and the SDK is correctly integrated into iMotions for real-time facial expression analysis.

> [!NOTE]
> This project assumes you have set up the iMotions data‐streaming APIs and configured the GSR electrodes (Shimmer3 or compatible) as well as the camera module for AFFDEX emotion detection.

---

## Installation
1. Clone repo
    ```bash
    git clone https://github.com/bbBerny/tiktok-engagement.git
    cd tiktok-engagement
    ```
2.  Create and activate a virtual environment
    ```bash
    python3 -m venv .venv
    ./.venv/Scripts/activate
    ```
3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

---

## Analysis methods
- **GSR feature extraction:**
    - Skin conductance detection using iMotions platform
    - Peak detection using SciPy
- **Facial expression analysis:** 
    - Engagement detection using iMotions platform
- **Statistical tests:**
    - One-sided binomial test to evaluate engagement proportions
    - Pearson correlation coefficients to explore how engagement evolved over time
    - Paired t-tests to determine whether engagement had a consistent effet on GSR

---

## Results
- **Key insights**
    - Engagement binarization suggests engagement responsiveness exceeded an established baseline
    - Engagement declined throughout the session
    - Facial engagement may not be always accompanied by an increased engagement response

---

## Visualization
- [!EngagementAndGsr](figures/Figure_1.png)
- [!EarlyVsLateEngagement](figures/Figure_2.png)

---

## Contact

If you have any questions or would like to collaborate, feel free to reach out:

- **Bernardo Sandoval**  
- **Email:** 0253019@up.edu.mx  
- **GitHub:** [github.com/bbBerny/tiktok-engagement](https://github.com/bbBerny/tiktok-engagement)





