# Restful Booker API Test Suite

Automated API tests for https://restful-booker.herokuapp.com
Built with Python, pytest, and requests.

## What's tested
- GET all bookings
- GET booking by ID (positive + negative)
- GET booking by name (valid, nonexistence, special characters, empty)
- POST create booking
- PUT full update
- PATCH partial update
- DELETE booking + verify deletion

## How to run
pip install -r requirements.txt
pytest -v

## Key decisions
- Session-scoped auth token fixture (login once, reuse across all tests)
- create_book fixture with yield for automatic cleanup
- parametrize for multiple similar negative cases
- timeout on all requests to prevent hanging tests


## Author
Emily | YYQ