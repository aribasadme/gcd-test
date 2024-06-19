# API Wrapper for ROKU TV Shows and Movies

This project provides an API wrapper to interact with two API endpoints and perform tasks such as retrieving TV shows/movies that can be played on the "ROKU" platform, filtering currently active items, and obtaining Level3 HD manifest paths for these active items. The script includes error handling and a retry mechanism for intermittent failures.

## Requirements

- Python 3.7 or higher
- `requests` library
- `python-dotenv` library

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/aribasadme/gcd-test.git
    cd gcd-test
    ```

2. **Create a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the root directory and add the following**:

    Replace `"<secret>"` with values from your provider
    ```
    API_ENDPOINT_1=<secret>
    API_ENDPOINT_2=<secret>
    API_USER=<secret>
    API_PASSWORD=<secret>
    ```

## Running the Script

1. **Run the script**:
    ```bash
    python main.py
    ```

2. **Expected Output**:

The script will log debug and info messages to the console and will print the Level3 HD manifest paths for currently active ROKU titles at the end.

## Code Overview
- **api_wrapper.py**: Contains the `APIWrapper` class that handles API requests, including error handling and retry logic.
- **utils.py**: Contains functions to retrieve titles playable on ROKU, filter currently active items, and get Level3 HD manifest paths.
- **config.py**: Loads configuration from environment variables.
- **main.py**: Main script that orchestrates the API calls and processes the data.
