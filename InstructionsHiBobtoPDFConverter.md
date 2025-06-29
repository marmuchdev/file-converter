# HiBob to PDF Converter Instructions

This guide explains how to export performance review data from HiBob as a JSON file and use the file-converter project to generate a ZIP file containing PDFs for each review (one PDF per reviewer).

---

## Prerequisites

- Access to a HiBob account with permission to view performance reviews.
- Docker Desktop installed and running.
- The file-converter repository cloned locally:
  ```bash
  git clone <repository-url>
A web browser (e.g., Chrome, Firefox) to access HiBob and download JSON files.

## Step-by-Step Instructions
1. Log in to HiBob
Open your web browser and navigate to https://app.hibob.com.

Log in with your HiBob credentials.

2. Switch to Talent Product
In the HiBob dashboard, locate the product switcher (usually in the top navigation bar).

Select Talent from the available Bob products.

3. Navigate to Performance Reviews
From the Talent dashboard, go to Performance in the left-hand menu.

Click on My Reviews to view your performance review cycles.

4. Access Manager Review
In the My Reviews section, find the review cycle you want to export.

Under the Managers Review section, click View to retrieve all reviews for the selected review cycle in a single JSON file, associated with one review ID.

5. Copy the Review ID from the URL
After clicking View, the browser URL will change to:

https://app.hibob.com/performance/my-reviews/reviews/{ID}/
Copy the {ID} from the URL (e.g., 1803723).

6. Construct the API URL
Create the API URL by appending the copied ID to:

https://app.hibob.com/api/reviews/{ID}/results/my
Example: If the ID is 1803723, the URL is:

https://app.hibob.com/api/reviews/1803723/results/my
7. Open the API URL in a Browser
Paste the constructed URL into your browser’s address bar and press Enter.

The browser will display the review data in JSON format.

8. Save the JSON File
Save the JSON data as a file:

Right-click the page and select Save As (or press Ctrl+S / Cmd+S).

Choose the .json file format and name the file descriptively, e.g., 6months_reviews.json.

9. Build the Project Using Docker
Ensure Docker Desktop is running.

Navigate to the cloned project directory:

bash
cd /path/to/file-converter
Build and start the Docker services:

bash
docker compose up --build
10. Access the HiBob to PDF Converter
Open your browser and go to http://localhost/hibob-to-pdf.

This loads the HiBob JSON to PDF Converter page.

11. Upload and Convert the JSON File
On the converter page, click the file input field to select the JSON file (e.g., 6months_reviews.json).

Click the Convert to PDF button.

The browser will download a file named hibob_reviews.zip.

12. Verify the Output
Extract the hibob_reviews.zip file to view the generated PDFs.

Each PDF corresponds to a single reviewer (e.g., manager or peer) and includes:

The review form title (e.g., "December 2024 Three Month Check-in (Manager Review)").

Reviewer name and type (e.g., "John Smith (Peer)").

Submission date.

Questions and answers from the review.

Example filename: December_2024_Three_Month_Check-in_(Peer_Review)_John_Smith.pdf

13. Repeat for Other Review Cycles
Repeat steps 4–12 for each additional review cycle you want to convert.

Save each JSON file with a unique name (e.g., 3months_reviews.json, annual_reviews.json) to avoid overwriting.

Notes
The converter supports JSON files with manager/peer reviews:

json
{
  "manager": {...},
  "peers": [...]
}
PDFs are generated with sanitized filenames (spaces replaced with underscores, invalid characters removed).

Ensure your HiBob API URL is accessible and you have permission to export review data.