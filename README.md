# Privacy Risk Assessment System

A comprehensive system for evaluating privacy risks in synthetic healthcare datasets by comparing them with real datasets.

## Prerequisites

Before you begin, make sure you have:
- Git installed
- Docker installed
- A terminal/command prompt

---

## Installation Guide

### macOS

#### Step 1: Install Git

1. Open Terminal
2. Install Homebrew (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Git:
   ```bash
   brew install git
   ```
4. Verify installation:
   ```bash
   git --version
   ```

#### Step 2: Install Docker

1. Download Docker Desktop for Mac from [docker.com](https://www.docker.com/products/docker-desktop)
2. Open the `.dmg` file and drag Docker to Applications folder
3. Open Applications and launch Docker
4. Wait for Docker to finish starting (you'll see the Docker menu icon in the top-right)
5. Verify installation:
   ```bash
   docker --version
   docker run hello-world
   ```

#### Step 3: Clone the Project

1. Open Terminal
2. Navigate to where you want to clone the project:
   ```bash
   cd ~/Documents
   ```
3. Clone the repository:
   ```bash
   git clone <repository-url>
   cd privacy-risk-assessment-system-CapstoneProject
   ```

#### Step 4: Create Environment Variables

1. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
2. Add the following content to `.env`:
   ```
   DB_NAME=privacy_risk
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_PORT=5432
   DATABASE_URL=postgresql://postgres:postgres@db:5432/privacy_risk
   ```

#### Step 5: Run the Project

1. Start the application using Docker Compose:
   ```bash
   docker compose up --build -d
   ```
2. Wait for all containers to start (this may take 1-2 minutes)
3. Open your browser and go to:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

#### To Stop the Project

```bash
docker compose down
```

---

### Windows

#### Step 1: Install Git

1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer and follow the setup wizard
3. Keep all default settings and click through to finish
4. Open Command Prompt or PowerShell and verify:
   ```bash
   git --version
   ```

#### Step 2: Install Docker

1. Download Docker Desktop for Windows from [docker.com](https://www.docker.com/products/docker-desktop)
2. Run the installer and follow the setup wizard
3. Restart your computer when prompted
4. Open Command Prompt or PowerShell and verify:
   ```bash
   docker --version
   docker run hello-world
   ```

#### Step 3: Clone the Project

1. Open Command Prompt or PowerShell
2. Navigate to where you want to clone the project:
   ```bash
   cd Documents
   ```
3. Clone the repository:
   ```bash
   git clone <repository-url>
   cd privacy-risk-assessment-system-CapstoneProject
   ```

#### Step 4: Create Environment Variables

1. Create a `.env` file in the project root
   - Open Notepad
   - Paste the following content:
   ```
   DB_NAME=privacy_risk
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_PORT=5432
   DATABASE_URL=postgresql://postgres:postgres@db:5432/privacy_risk
   ```
   - Save as `.env` in the project root directory

2. Or use PowerShell:
   ```bash
   @"
   DB_NAME=privacy_risk
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_PORT=5432
   DATABASE_URL=postgresql://postgres:postgres@db:5432/privacy_risk
   "@ | Out-File -Encoding UTF8 .env
   ```

#### Step 5: Run the Project

1. Open PowerShell or Command Prompt in the project directory
2. Start the application:
   ```bash
   docker compose up --build -d
   ```
3. Wait for all containers to start (this may take 1-2 minutes)
4. Open your browser and go to:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

#### To Stop the Project

```bash
docker compose down
```

---

## Project Structure

```
privacy-risk-assessment-system/
├── backend/              # FastAPI backend server
├── frontend/             # Next.js React frontend
├── docker-compose.yml    # Docker configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

---

## Features

- **Upload Datasets**: Upload real and synthetic healthcare datasets
- **Privacy Analysis**: Evaluate privacy risks using advanced metrics
- **Visual Reports**: View detailed privacy risk assessments
- **Comparative Analysis**: Compare synthetic vs real data privacy

---

## Troubleshooting

### Docker won't start
- Restart Docker Desktop
- Ensure virtualization is enabled in BIOS (Windows)

### Port already in use
- Change port numbers in `docker-compose.yml`
- Or kill the process using the port:
  - **macOS/Linux**: `lsof -ti:3000 | xargs kill -9`
  - **Windows**: `netstat -ano | findstr :3000` then `taskkill /PID <PID> /F`

### Database connection error
- Ensure `.env` file is created correctly
- Wait 30 seconds after running `docker compose up` for the database to initialize

---

## Support

For issues or questions, please open an issue in the repository or contact the development team.

---

## License

This project is part of a capstone project.
