# Dependencies

## Required Python Packages

This project requires the following Python packages:

### Core Dependencies
- **google-genai** (>=0.8.0) - Google's Generative AI client library
- **numpy** (>=1.24.0) - Numerical computing library for similarity calculations

### Installation

#### Using pip:
```bash
pip install google-genai numpy
```

#### Using conda:
```bash
conda install numpy
pip install google-genai
```

#### Using Replit:
The packages are automatically installed when you run the project on Replit.

## Python Version
- **Python 3.8+** required
- **Python 3.11+** recommended

## External Services
- **Google Gemini API** - Requires API key from https://aistudio.google.com/

## Optional Dependencies
- None - this project uses only standard library modules and the core dependencies listed above

## Verification

Run the setup script to verify all dependencies:
```bash
python setup.py
```

This will check:
- Python version compatibility
- Package installation status
- API key configuration
- Storage file creation