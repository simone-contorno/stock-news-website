# Stock News Website with Interactive Graphs

A web application that displays daily performance of stock indices and individual stocks using interactive graphs, along with relevant news articles that may influence market movements.

## Features

- Interactive stock price charts with various timeframes
- Daily stock market news with sentiment analysis
- Correlation between news sentiment and stock price movements
- Responsive design for desktop and mobile devices

## Technology Stack

### Backend
- Python 3.9+ with FastAPI
- PostgreSQL for structured data
- MongoDB for unstructured data
- Celery with Redis for task scheduling
- Data processing with pandas, NumPy, spaCy, and NLTK

### Frontend
- React.js with Redux for state management
- Material-UI for components
- Highcharts for data visualization

## Project Structure

```
├── backend/               # FastAPI application
│   ├── app/              # Application code
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── db/           # Database models and connections
│   │   ├── services/     # Business logic
│   │   └── tasks/        # Celery tasks
│   ├── tests/            # Backend tests
│   └── requirements.txt  # Python dependencies
├── frontend/             # React application
│   ├── public/           # Static files
│   ├── src/              # Source code
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── store/        # Redux store
│   │   └── utils/        # Utility functions
│   ├── package.json      # NPM dependencies
│   └── README.md         # Frontend documentation
└── docker/               # Docker configuration
    ├── backend/          # Backend Dockerfile
    ├── frontend/         # Frontend Dockerfile
    └── docker-compose.yml # Docker Compose configuration
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 14+
- Docker and Docker Compose (optional)
- PostgreSQL
- MongoDB
- Redis

### Installation

1. Clone the repository
2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. Start the backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
2. Start the frontend:
   ```bash
   cd frontend
   npm start
   ```

## License

MIT