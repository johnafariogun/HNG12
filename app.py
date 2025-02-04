"""
FastAPI application for classifying numbers based on mathematical properties.

This API determines whether a given number is:
- Prime
- Perfect
- Armstrong
- Odd/Even

It also provides the digit sum and a fun fact about the number using the Numbers API.
"""
import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import aiohttp
import numpy as np

# Initialize FastAPI app
app = FastAPI(
    title="Number Classification API",
    description="An API to classify numbers based on mathematical properties.",
    version="1.0.0",
)

# Enable CORS for specified origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hng12-owcr.onrender.com"],
    allow_methods=["GET"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Process pool executor for CPU-bound tasks
process_executor = ProcessPoolExecutor()

def is_prime(num: int) -> bool:
    """
    Check if a number is prime.

    Args:
        num (int): The number to check.

    Returns:
        bool: True if the number is prime, False otherwise.
    """
    if num < 2:
        return False
    if num in (2, 3):
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    divisors = np.arange(5, int(np.sqrt(abs(num))) + 1, 6)
    return not np.any(abs(num) % divisors == 0) and not np.any(abs(num) % (divisors + 2) == 0)

def is_perfect(n: int) -> bool:
    """
    Check if a number is a perfect number.

    A perfect number is a positive integer that is equal to the sum of its proper divisors.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if the number is perfect, False otherwise.
    """
    if n < 2:
        return False
    total = 1  # Start with 1 because it's a divisor for all numbers
    for i in range(2, int(np.sqrt(abs(n))) + 1):
        if n % i == 0:
            total += i
            if i != n // i:  # Avoid adding the same divisor twice for perfect squares
                total += n // i
    return total == abs(n)

def is_armstrong(num: int) -> bool:
    """
    Check if a number is an Armstrong number.

    An Armstrong number is a number that is equal to the sum of its own digits each raised to the power of the number of digits.

    Args:
        num (int): The number to check.

    Returns:
        bool: True if the number is an Armstrong number, False otherwise.
    """
    digits = np.array(list(map(int, str(abs(num)))))
    return abs(num) == np.sum(digits ** len(digits))

def digit_sum(num: int) -> int:
    """
    Calculate the sum of the digits of a number.

    Args:
        num (int): The number to calculate the digit sum for.

    Returns:
        int: The sum of the digits of the number.
    """
    return np.sum(np.array(list(map(int, str(abs(num))))))

async def get_fun_fact(num: int) -> str:
    """
    Fetch a fun fact about the number from the Numbers API.

    Args:
        num (int): The number to fetch a fun fact for.

    Returns:
        str: A fun fact about the number or a default message if no fact is found.
    """
    url = f"http://numbersapi.com/{num}?json&math=true"
    try:
        async with aiohttp.ClientSession() as session, session.get(url, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("text", "No fun fact available.")
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return "No fun fact found."

@app.get("/api/classify-number", response_model=dict)
async def classify_number(number: Union[int, str]) -> JSONResponse:
    """
    Classify a given number based on its mathematical properties.

    Args:
        number (Union[int, str]): The number to classify, received as a query parameter.

    Returns:
        JSONResponse: A JSON response containing:
            - number: The input number.
            - is_prime: Whether the number is prime.
            - is_perfect: Whether the number is perfect.
            - properties: List of properties (Armstrong, Odd/Even).
            - digit_sum: Sum of the digits of the number.
            - fun_fact: A mathematical fact about the number.

    If ValueError Returns:
        JSONResponse: A JSON response containing:
        - number: the invalid iput(alphabet)
        - error: true
    """
    try:
        number = int(number)
    except ValueError:
        return JSONResponse(status_code=400, content={"number": number, "error": True})

    # Offload CPU-bound tasks to the process pool
    loop = asyncio.get_running_loop()
    is_prime_number = await loop.run_in_executor(process_executor, is_prime, number)
    is_perfect_number = await loop.run_in_executor(process_executor, is_perfect, number)
    is_armstrong_number = await loop.run_in_executor(process_executor, is_armstrong, number)
    digit_sum_value = await loop.run_in_executor(process_executor, digit_sum, number)

    # Convert NumPy boolean values to native Python boolean values
    is_prime_number = bool(is_prime_number)
    is_perfect_number = bool(is_perfect_number)
    is_armstrong_number = bool(is_armstrong_number)

    properties = ["armstrong"] if is_armstrong_number else []
    properties.append("odd" if number % 2 else "even")

    # Fetch fun fact asynchronously
    fun_fact = await get_fun_fact(number)

    return JSONResponse(content={
        "number": number,
        "is_prime": is_prime_number,
        "is_perfect": is_perfect_number,
        "properties": properties,
        "digit_sum": int(digit_sum_value),  # Ensure digit_sum is an integer
        "fun_fact": fun_fact
    })