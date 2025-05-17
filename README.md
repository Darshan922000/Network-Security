# Network Security Project - Phishing Detection

This is an End-to-End Machine Learning project focused on Network Security, specifically for detecting phishing attempts. The project implements a complete ML pipeline from data ingestion to model deployment.

## Project Structure

```
├── app.py                 # FastAPI application for model serving
├── main.py               # Main application entry point
├── etl_pipeline.py       # ETL pipeline implementation
├── Dockerfile            # Docker configuration for containerization
├── pyproject.toml        # Project dependencies and metadata
├── poetry.lock          # Locked dependencies
├── templates/           # HTML templates for web interface
├── final_model/         # Trained model artifacts
├── Network_Data/        # Dataset directory
├── Notebooks/           # Jupyter notebooks for analysis
├── networksecurity/     # Core project package
├── valid_data/          # Validation data
└── Prediction Output/   # Directory for prediction results
```

## Features

- FastAPI-based web application for model serving
- MongoDB integration for data storage
- Docker containerization support
- Complete ML pipeline implementation
- Interactive web interface for predictions
- Model training and prediction endpoints

## Setup and Installation

1. Clone the repository
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Set up environment variables:
   - Create a `.env` file with your MongoDB connection string:
     ```
     MONGODB_URL=your_mongodb_connection_string
     ```

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Access the API documentation at `http://localhost:8000/docs`

3. Available endpoints:
   - `/train` - Train the model
   - `/predict` - Make predictions using the trained model
   - `/` - Redirects to API documentation

## Model Training

The project includes a complete training pipeline that can be triggered through the `/train` endpoint. The pipeline handles:
- Data ingestion
- Preprocessing
- Model training
- Model evaluation
- Model persistence

## Prediction

The `/predict` endpoint accepts CSV files containing network data and returns predictions for potential phishing attempts. Results are displayed in an interactive web interface.

## Docker Support

The project can be containerized using the provided Dockerfile:
```bash
docker build -t network-security .
docker run -p 8000:8000 network-security
```

## Development

- Python 3.10.11
- FastAPI
- MongoDB
- Poetry for dependency management
- Docker for containerization

## License

This project is licensed under the MIT License.