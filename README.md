
# DNS Health Check API

This is a FastAPI application that analyzes the DNS health of a given domain, using a custom-built DNSSEC analyzer tool. The results are stored in a MongoDB database.

## Project Structure

```
DNS-HEALTH/
├── app/
│   ├── __pycache__/       # Compiled Python files
│   ├── dns.py             # Module for DNS health analysis
│   ├── models.py          # MongoDB-related connections and data models
│   ├── test.py            # Testing file for the application
├── dnssec-analyzer/       # Directory for the DNSSEC analyzer Go binary
├── env/                   # Virtual environment (not included in version control)
├── main.py                # Main FastAPI application file
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
```

## Setup and Installation

### Prerequisites

- **Python** (>= 3.8)
- **MongoDB** (running on `localhost:27017`)
- **Go** (to compile the DNSSEC analyzer tool, if not already compiled)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/DNS-HEALTH.git
cd DNS-HEALTH
```

### 2. Set Up Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Compile the DNSSEC Analyzer (Go)

If the DNSSEC analyzer is not already compiled, navigate to the `dnssec-analyzer` directory and compile it:

```bash
cd dnssec-analyzer
go build -o dnssec-analyzer.exe ./cmd/dnssec-analyzer
```

Ensure the compiled binary (`dnssec-analyzer.exe` on Windows) is located in the `dnssec-analyzer` folder.

### 5. Configure MongoDB

Ensure MongoDB is running on `localhost:27017`. This application uses a MongoDB database named `DNS` and a collection named `dns_analyses`.

### 6. Run the Application

Navigate back to the root directory and start the FastAPI application:

```bash
uvicorn main:app --reload
```

### 7. Access the API Documentation

Visit `http://127.0.0.1:8000/docs` in your browser to see the interactive API documentation.

## API Endpoints

### 1. **POST** `/start-analysis`

- **Description**: Start DNS health analysis for a given domain.
- **Request Body**:
  ```json
  {
    "domain": "example.com"
  }
  ```
- **Response**:
  - `200 OK` if successful
  - JSON result:
    ```json
    {
      "_id": "unique-analysis-id",
      "domain": "example.com",
      "result": {
        "domain": "example.com",
        "status": "healthy",
        "error": "No RRSIGs found"
      },
      "timestamp": "2024-11-12 12:00:00"
    }
    ```

### 2. **GET** `/get-analysis/{analysis_id}`

- **Description**: Retrieve DNS analysis results by analysis ID.
- **Response**:
  - `200 OK` if found, `404 Not Found` if not found
  - JSON result:
    ```json
    {
      "_id": "unique-analysis-id",
      "domain": "example.com",
      "result": {
        "domain": "example.com",
        "status": "healthy",
        "error": "No RRSIGs found"
      },
      "timestamp": "2024-11-12 12:00:00"
    }
    ```

## Code Overview

- **`main.py`**: Initializes the FastAPI app and defines the API endpoints.
- **`app/dns.py`**: Contains the `analyze_dns_health` function to interact with the DNSSEC analyzer tool.
- **`app/models.py`**: Defines the MongoDB interaction functions to save and retrieve analysis results.
- **`app/test.py`**: Contains test cases for the API (not fully implemented).
- **`dnssec-analyzer/`**: Directory for the DNSSEC analyzer tool (compiled from Go).

## Example Usage

To analyze the health of `google.com`, you can use the following `curl` command:

```bash
curl -X 'POST'   'http://127.0.0.1:8000/start-analysis'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "domain": "google.com"
}'
```

This will return a JSON object with the analysis ID and result.

## Running Tests

If tests are implemented in `test.py`, you can run them using:

```bash
python app/test.py
```

## License

This project is licensed under the MIT License.

---

Replace any placeholders, such as `yourusername` in the repository link, with your actual information. This `README.md` file provides a comprehensive guide on setting up, running, and using the DNS Health Check API based on your project structure.
