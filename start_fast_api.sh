#!/bin/bash

# Set environment variables
export ADMIN_SECRET='Hi'
export DATABASE_URL='sqlite:///euanh_website.db'
export RECAPTCHA_SITE_KEY='example'
export RECAPTCHA_SECRET_KEY='example'

# Run the application with Poetry
poetry run tailwindcss -i app.css -o .\euanh_website\static\css\tailwind.css --minify
poetry run uvicorn euanh_website.main:app --reload
