# Smart ML Model Trainer - ML Training Platform

A full-stack machine learning training and comparison platform with a futuristic terminal-inspired interface. Train, evaluate, and compare multiple ML models with an intuitive dashboard.

<img width="1898" height="904" alt="image" src="https://github.com/user-attachments/assets/ce3fe705-36d0-429b-a554-5ecfa86d1e96" />


## Features

### Core Capabilities
- **Dataset Management**: Upload CSV/Excel files or fetch datasets directly from Kaggle
- **Automated Data Cleaning**: Handle missing values, remove duplicates, and encode categorical variables
- **Supervised Learning**: Classification and regression models with comprehensive metrics
- **Unsupervised Learning**: Clustering and dimensionality reduction algorithms
- **Model Comparison**: Side-by-side comparison of two models with visual analytics
- **Real-time Training Progress**: Live progress tracking with status updates
- **Model Export**: Download trained models for deployment

### Supported Models

#### Supervised Learning
#### Unsupervised Learning

## Project Structure

```
CompareModel-main/
├── backend/
│   ├── server.py              # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── models/                # Saved model files (.pkl)
│   ├── uploads/               # Uploaded datasets
│   └── visualizations/        # Generated charts
├── frontend/
│   ├── src/
│   │   ├── pages/            # React pages
│   │   ├── components/       # Reusable components
│   │   ├── lib/              # Utilities
│   │   └── App.js            # Main app component
│   ├── package.json          # Node dependencies
│   └── .env                  # Environment variables
├── design_guidelines.json    # UI/UX design system
└── README.md                 # This file
```
## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: MongoDB (via Motor async driver)
- **ML Libraries**: scikit-learn, XGBoost, pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Data Processing**: pandas, numpy

### Frontend
- **Framework**: React 18
- **UI Components**: Radix UI, shadcn/ui
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Routing**: React Router v7

## Prerequisites
- Python 3.8+
- Node.js 16+ and Yarn
- MongoDB instance (local or cloud)
- Kaggle API credentials (optional, for Kaggle dataset integration)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd CompareModel-main
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create a .env file with:
MONGO_URL=mongodb://localhost:27017
DB_NAME=ml_platform
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
yarn install

# Configure environment variables
# Create a .env file with:
REACT_APP_API_URL=http://localhost:8000
```

## Running the Application

### Start Backend Server
```bash
cd backend
uvicorn server:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Start Frontend Development Server
```bash
cd frontend
yarn start
```

## Usage Guide

### 1. Upload Dataset
### 2. Data Cleaning
### 3. Model Selection
### 4. Model Configuration
### 5. Training
### 6. Results & Visualization
**Classification Metrics:**
- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix heatmap
- ROC Curve (binary classification)
### 7. Model Comparison
- Select two models to compare
- Configure parameters for both
- View side-by-side metrics and visualizations
- Identify the better performing model

Built with ❤️ using FastAPI and React
