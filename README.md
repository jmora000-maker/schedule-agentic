# Schedule Risk Case Management

A Streamlit-based application for automated schedule risk analysis and case management. This tool helps identify potential schedule slips by processing project documentation.

## Features

- **Automated Pipeline**: Execute schedule risk analysis on project documents.
- **Case Management**: View, sort, and manage identified risk cases.
- **Risk Assessment**: Visualize risk severity and confidence scores.
- **Evidence Inspection**: Deep dive into evidence supporting each identified risk.

## Prerequisites

- Python 3.10+
- OpenAI API Key

## Setup

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key in your environment variables:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   # Or use a .env file
   ```

## Usage

1. Place your project documents (e.g., DOCX, CSV, XML) in the `data/` folder.
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open the provided local URL in your browser.
4. Click "Execute Schedule Risk Pipeline" to begin analysis.
