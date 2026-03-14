# Privacy Risk Assessment System for Synthetic Healthcare Datasets

Capstone project for evaluating privacy risks in synthetic healthcare datasets.

## Project Overview
This system is designed to help users assess whether synthetic healthcare datasets preserve privacy adequately before sharing or using them. The platform allows users to upload real and synthetic datasets, define quasi-identifiers and sensitive attributes, run privacy risk evaluations, and review results through an interactive dashboard and exportable reports.

## Core Features
- Upload real and synthetic datasets
- Define quasi-identifiers and sensitive attributes
- Run privacy risk evaluations such as:
  - Re-identification / linkage risk
  - Membership inference risk
  - Attribute inference risk
  - Uniqueness / rare combination risk
- Visualize results in an interactive dashboard
- Export privacy audit reports

## Suggested Tech Stack
### Frontend
- React or Next.js

### Backend
- Python
- FastAPI
- pandas / numpy / scipy
- scikit-learn

### Database
- PostgreSQL

### DevOps / Deployment
- Docker
- docker-compose

## Repository Structure
```text
privacy-risk-assessment-system/
├── backend/
│   └── app/
├── frontend/
│   └── src/
├── docs/
├── datasets/
│   └── sample_data/
├── sql/
├── tests/
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Folder Purpose
- `backend/` - FastAPI backend and privacy evaluation logic
- `frontend/` - UI/dashboard code
- `docs/` - proposal, meeting notes, diagrams, reports
- `datasets/sample_data/` - non-sensitive demo or synthetic sample datasets only
- `sql/` - SQL scripts and schema files
- `tests/` - test cases for backend/frontend modules

## Setup Instructions
1. Clone the repository
2. Create backend and frontend environments
3. Configure environment variables in `.env` files (do not commit them)
4. Run services locally or with Docker
5. Start development

Example:
```bash
git clone https://github.com/your-username/privacy-risk-assessment-system.git
cd privacy-risk-assessment-system
```

## Team Members
- Faisal Ahmed
- Manvi Singh
- Rodney Karlo Pascual
- Tharu Sanudha Kawmadi Weerasinghe

## Notes
- Do not upload real private healthcare datasets to GitHub
- Use only synthetic or safe sample datasets in this repository
- Keep credentials and `.env` files private
