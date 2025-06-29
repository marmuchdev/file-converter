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

```

```
