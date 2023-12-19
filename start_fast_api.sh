#!/bin/bash

# Set environment variables
export ADMIN_SECRET='Hi'
export DATABASE_URL='sqlite:///euanh_website.db'

# Run the application with Poetry
poetry run tailwindcss -i app.css -o .\euanh_website\static\css\tailwind.css --minify
poetry run uvicorn euanh_website.main:app --reload
