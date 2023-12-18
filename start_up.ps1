# Set environment variables
$env:ADMIN_SECRET = 'Hi'
$env:DATABASE_URL = 'sqlite:///euanh_website.db'

# Run the application with Poetry
poetry run uvicorn euanh_website.main:app --reload
