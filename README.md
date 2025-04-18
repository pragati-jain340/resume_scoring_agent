# Resume Scoring Agent

A Python application that automatically scores and processes resumes.

## Features
- Resume parsing and analysis
- Automated scoring based on criteria
- Email notification system
- Logging and output generation

## Folder Structure
```
resume_scoring_agent/
├── config.py            - Configuration settings
├── emailer.py           - Email notification system
├── main.py              - Main application logic
├── scoring.py           - Scoring algorithms
├── utils.py             - Utility functions
├── logs/                - Process logs
├── output/              - Generated reports
├── processed/           - Processed resumes (empty - .gitkeep maintains structure)
├── resumes/             - Input resumes
└── .gitignore           - Git ignore rules
```

## Setup
1. Clone repository:
   ```bash
   git clone https://github.com/pragati-jain340/resume_scoring_agent.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
```bash
python main.py
```

## Maintained Folder Structure
The `processed/` folder is kept in the repository with a `.gitkeep` file to maintain directory structure while remaining empty in development.