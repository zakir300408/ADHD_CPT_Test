# ADHD Continuous Performance Task (CPT) Test

A graphical application for administering a Continuous Performance Task (CPT) test to assess attention and impulsivity, commonly used in ADHD evaluation.

## Overview

This application provides a digital implementation of the Continuous Performance Task, which is commonly used in neuropsychological assessments. It presents a series of stimuli (letters) to the user, who must respond only to a specific target stimulus while ignoring others.

## Features

- User-friendly GUI interface
- Customizable test parameters
- Real-time test administration
- Comprehensive results with metrics:
  - Hit rate (correct responses to targets)
  - False alarm rate (incorrect responses to non-targets)
  - Omission errors (missed targets)
  - Commission errors (responses to non-targets)
  - Response time statistics
  - D-prime sensitivity index
- Visual reports with graphs and charts
- Export results as CSV and HTML reports with PNG visualizations

## Installation

1. Make sure you have Python 3.7 or newer installed
2. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

Run the application:

```
python adhd_cpt.py
```

Follow the on-screen instructions to:
1. Enter participant information
2. Read the test instructions
3. Complete the CPT test
4. View and save results

## Test Description

In this implementation:
- The test runs for 5 minutes (300 seconds)
- Letters appear on the screen one at a time
- The participant must press the spacebar when they see the target letter 'X'
- The participant should not respond to any other letter
- The test measures attention (ability to respond to targets) and impulsivity (ability to inhibit responses to non-targets)

## Interpretation

Results include:
- **Hit Rate**: Proportion of correctly identified targets. Lower scores may indicate inattention.
- **False Alarm Rate**: Proportion of incorrect responses to non-targets. Higher scores may indicate impulsivity.
- **Mean Response Time**: Average time to respond to targets. Slow or variable response times may indicate attention issues.
- **d'**: A sensitivity index that accounts for both hit rate and false alarm rate.

## License

MIT
