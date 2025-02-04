# FastAPI Number Classification API

## Overview
This FastAPI application classifies numbers based on their mathematical properties. The API determines whether a given number is:
- **Prime**
- **Perfect**
- **Armstrong**
- **Odd/Even**

Additionally, it calculates the **sum of the digits** of the number and fetches a **fun fact** about the number from the Numbers API.

## Features
- **Prime Number Check**: Determines if a number is prime.
- **Perfect Number Check**: Identifies whether a number is a perfect number.
- **Armstrong Number Check**: Checks if a number is an Armstrong number.
- **Odd/Even Classification**: Determines if a number is odd or even.
- **Digit Sum Calculation**: Computes the sum of all digits in a number.
- **Fun Fact Retrieval**: Fetches a mathematical fun fact about the number from the Numbers API.
- **CORS Support**: Enabled for `https://hng12-owcr.onrender.com`.

## Installation
### Prerequisites
- Python 3.8+
- FastAPI
- Uvicorn
- Aiohttp

### Setup
1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   cd fastapi-number-classifier
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the API**
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints
### 1. Classify a Number
- **Endpoint**: `GET /api/classify-number`
- **Query Parameter**: `number` (integer as a string)
- **Response Format**:
  ```json
  {
    "number": 6,
    "is_prime": false,
    "is_perfect": true,
    "properties": ["even", "armstrong"],
    "digit_sum": 6,
    "fun_fact": "6 is the first perfect number."
  }
  ```

## Deployment
This API is designed to be deployed on **Render** [Visit Classify API](https://hng12-owcr.onrender.com/api/classify-number?number=371), but it can also run on other cloud services.

To deploy on **Render**:
1. Push your repository to GitHub.
2. Link your repository to Render and select **FastAPI** as the runtime.
3. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
4. Deploy and access your API.

## License
This project is licensed under the MIT License.

## Author
Developed by **John Tolulope Afariogun** 🚀.

