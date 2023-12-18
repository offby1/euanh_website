#!/bin/bash

# Set environment variables
export ADMIN_SECRET='Hi'
export DATABASE_URL='sqlite:///euanh_website.db'

# Run the application with Poetry
poetry run uvicorn euanh_website.main:app --reload
