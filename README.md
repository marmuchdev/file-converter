# File Converter

A web application with a React Vite frontend and Flask backend to convert JSON files to PDF, with a modular design for adding more converters in the future.

## Project Structure

- `client/`: React Vite frontend with navigation (Home, Converters, JSON to PDF).
- `server/`: Flask backend with a blueprint-based structure for converters.

## Setup Instructions

### Backend (Flask)

1.  Navigate to `server/`:
    ```bash
    cd server
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the Flask server:
    ```bash
    python main.py
    ```

### Frontend (React Vite)

1.  Navigate to `client/`:
    ```bash
    cd client
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```

### Docker Setup

1.  Ensure Docker and Docker Compose are installed.
2.  From the project root, build and run the containers:
    ```bash
    docker compose up --build
    ```
3.  Access the app at `http://localhost:80`.
4.  Stop the containers:
    ```bash
    docker compose down
    ```

### Usage

- Open `http://localhost:80` in your browser.
- Navigate to "Converters" > "JSON to PDF".
- Upload a JSON file and click "Convert to PDF" to download the result.

## Adding New Converters

- **Backend**: Add a new blueprint in `server/app/converters/` (e.g., `csv_to_pdf.py`) and register it in `server/app/__init__.py`.
- **Frontend**: Add a new page in `client/src/pages/` (e.g., `CsvToPdf.jsx`), update `App.jsx` with a new route, and update `Converters.jsx` to list it.

## Testing the Application

### Frontend Testing Locally

The frontend uses Vitest for unit testing React components in the `client/` directory.

1.  **Navigate to the frontend directory**:

    ```
    cd client

    ```

2.  **Install test dependencies**:

    ```
    npm install -D vitest @vitest/ui jsdom @testing-library/react @testing-library/jest-dom msw

    ```

3.  **Run tests**:

    ```
    npm run test

    ```

    This executes all tests in `tests/` (e.g., `Home.test.jsx`, `Converters.test.jsx`, `JsonToPdf.test.jsx`).

4.  **Run tests interactively** (optional):

    ```
    npm run test:watch

    ```

    This runs Vitest in watch mode for development.

### Backend Testing Locally

The backend uses pytest for unit testing Flask endpoints in the `server/` directory.

1.  **Navigate to the backend directory**:

    ```
    cd server

    ```

2.  **Activate the virtual environment**:

    ```
    source venv/bin/activate

    ```

3.  **Install test dependencies**:

    ```
    pip install pytest pytest-flask

    ```

4.  **Run tests**:

    ```
    pytest

    ```

    This executes all tests in `tests/` (e.g., `test_json_to_pdf.py`).

### Frontend Testing with Docker

The frontend tests can be run in a Docker container using the `frontend-test` service.

1.  **Navigate to the project root**:

    ```
    cd ~/dev/file-converter

    ```

2.  **Build and run the test container**:

    ```
    docker compose up --build frontend-test

    ```

    This builds the `frontend-test` service using `client/Dockerfile.test` (or the `builder` stage of `client/Dockerfile`) and runs `npm run test`.

3.  **View test output**:

    -   Test results are displayed in the container logs.
    -   To debug, check logs:

        ```
        docker logs file-converter-frontend-test-1

        ```

**Note**: Ensure `client/Dockerfile.test` exists or `docker-compose.yml` targets the `builder` stage of `client/Dockerfile` with a Node.js environment (e.g., `node:20.19.3`).
