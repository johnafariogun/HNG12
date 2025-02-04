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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Union
import aiohttp

app = FastAPI()

# Enable CORS for specified origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hng12-owcr.onrender.com"],
    allow_methods=["GET"],
    allow_headers=["*"],
    allow_credentials=True,
)


def is_prime(num: int) -> bool:
    """Check if a number is prime."""
    if num < 2:
        return False
    if num in (2, 3):
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True


def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    if n < 2:
        return False
    return sum(i for i in range(1, n // 2 + 1) if n % i == 0) == n


def is_armstrong(num: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = list(map(int, str(num)))
    return num == sum(d ** len(digits) for d in digits)


def digit_sum(num: int) -> int:
    """Calculate the sum of digits of a number."""
    return sum(map(int, str(num)))


async def get_fun_fact(num: int) -> str:
    """Fetch a fun fact about the number from the Numbers API."""
    url = f"http://numbersapi.com/{num}?json&math=true"
    try:
        async with aiohttp.ClientSession() as session, session.get(url, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("text", "No fun fact available.")
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return "No fun fact found."


@app.get("/api/classify-number")
async def classify_number(number: Union[int, str]):
    """
    Classify a given number based on its mathematical properties.

    Parameters:
    - number (int, str): The number to classify, received as a query parameter.

    Returns:
    - JSON response with properties:
      - is_prime: Whether the number is prime.
      - is_perfect: Whether the number is perfect.
      - properties: List of properties (Armstrong, Odd/Even).
      - digit_sum: Sum of the digits of the number.
      - fun_fact: A mathematical fact about the number.
    """
    try:
        number = int(number)
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"number": number, "error": True},
        )

    is_prime_number = is_prime(number)
    is_perfect_number = is_perfect(number)
    is_armstrong_number = is_armstrong(number)
    digit_sum_value = digit_sum(number)
    properties = ["armstrong"] if is_armstrong_number else []
    properties.append("odd" if number % 2 else "even")

    fun_fact = await get_fun_fact(number)

    return JSONResponse(content={
        "number": number,
        "is_prime": is_prime_number,
        "is_perfect": is_perfect_number,
        "properties": properties,
        "digit_sum": digit_sum_value,
        "fun_fact": fun_fact
    })
