# 🌐 Website Uptime Monitoring Dashboard

A lightweight Python application for checking whether a website is reachable, measuring its HTTP response time, and storing monitoring results in a local SQLite database.

The project uses Streamlit to provide a simple browser-based dashboard. It was developed as a student project to learn about website availability monitoring, HTTP requests, data storage, and basic performance analysis.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Run the Application](#run-the-application)
- [How to Use](#how-to-use)
- [Understanding the Results](#understanding-the-results)
- [Database](#database)
- [Exporting Data](#exporting-data)
- [Current Scope and Limitations](#current-scope-and-limitations)
- [Future Improvements](#future-improvements)
- [Troubleshooting](#troubleshooting)
- [Responsible Use](#responsible-use)
- [Author](#author)

---

## Project Overview

Website availability is important for many online services, including educational portals, e-commerce websites, government portals, and information systems. When a website becomes unavailable or slow to respond, users may be unable to access the service.

This project is a basic monitoring dashboard that allows a user to:

1. Enter a website URL.
2. Send an HTTP GET request.
3. Check the returned HTTP status code.
4. Measure the time taken for the request to complete.
5. Save the result with a timestamp.
6. Review previous checks and response-time trends.

The application is designed as an educational prototype. It performs checks when the user clicks the button manually and is not intended to function as a fully unattended monitoring service.

## Features

- Website availability check for HTTP/HTTPS URLs
- HTTP status code display
- Response-time measurement in milliseconds
- Online/offline classification based on server response
- Monitoring history stored in SQLite
- Observed availability calculation for the most recently checked website
- Response-time chart for recent checks
- CSV export of monitoring history for analysis and reporting

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Browser-based dashboard interface |
| Requests | Sends HTTP requests to target websites |
| SQLite | Stores monitoring records locally |
| Pandas | Reads and structures monitoring data |
| Matplotlib | Visualises response-time trends |

## Project Structure

```text
Website_Uptime_Monitor_Project/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python package dependencies
├── README.txt              # Project documentation
├── monitoring.db           # SQLite database generated at runtime
├── py.bat                  # Optional Windows launcher/helper script
└── .venv                   # Local virtual environment (if created)
```

The `monitoring.db` file is created automatically when the application runs for the first time. It stores the monitoring records locally on the user’s device.

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or later
- Visual Studio Code or another Python editor
- Internet connection for checking public websites
- Modern web browser

This project does not require paid cloud services or special hardware for local use.

## Installation

### 1. Download or extract the project

If you downloaded the project as a ZIP file, extract it to a folder on your computer.

### 2. Open the project in VS Code

1. Open Visual Studio Code.
2. Select File → Open Folder.
3. Choose the project folder.
4. Open Terminal → New Terminal.

### 3. Check Python

Run the following command in the terminal:

```powershell
py --version
```

If Python is installed, the terminal should display a version number similar to:

```text
Python 3.12.4
```

If the `py` command is unavailable, install Python from python.org and make sure the Add Python to PATH option is selected during installation.

### 4. Install dependencies

From the project folder, run:

```powershell
py -m pip install -r requirements.txt
```

If the requirements file is not available, install the packages manually:

```powershell
py -m pip install streamlit requests pandas matplotlib
```

Wait for installation to complete before starting the app.

## Run the Application

From the project folder, run:

```powershell
py -m streamlit run app.py
```

Streamlit will start a local web server and usually open the dashboard in the default browser.

If the browser does not open automatically, copy the Local URL shown in the terminal (commonly `http://localhost:8501`) and open it manually.

To stop the app, press:

```text
Ctrl + C
```

## How to Use

1. Start the application with the command above.
2. Go to the left sidebar and locate Monitor a website.
3. Enter a valid URL, such as `https://example.com`.
4. Click Check now.
5. Read the status message, HTTP status code, and response time.
6. Review the monitoring history and charts on the main page.
7. Repeat checks to collect more observations.
8. Use the CSV download button to export the monitoring history.

The app automatically adds `https://` when a URL does not include a scheme.

## Understanding the Results

### Website status

- Online: the website returned an HTTP status code below 400.
- Offline: the request failed, timed out, or returned a status code of 400 or higher.

This is a simplified classification intended for a basic educational prototype. Some websites may return an error status even when the server is reachable.

### HTTP status code

An HTTP status code indicates the result of the request. Examples include:

- `200` — OK
- `301` or `302` — redirect
- `403` — forbidden
- `404` — not found
- `500` — server error

This project follows redirects automatically, so the recorded code is generally the final response code returned by the target website.

### Response time

Response time is measured by the client application and shown in milliseconds (ms). It represents the elapsed time required for the HTTP request to complete, not a direct measurement of server-side processing alone.

### Observed availability

The dashboard calculates the observed availability using:

```text
Observed availability (%) = (Number of successful checks / Total checks) × 100
```

For example, if 9 out of 10 checks are successful:

```text
Observed availability = (9 / 10) × 100 = 90%
```

This metric reflects only the checks stored in the local database and is not a formal SLA or guarantee of long-term uptime.

## Database

The application uses SQLite, which is included with Python.

The database file is named:

```text
monitoring.db
```

Each stored record includes:

- website URL
- status (`Online` or `Offline`)
- response time in milliseconds
- HTTP status code
- date and time of the check
- error message, if the request failed

Do not delete `monitoring.db` if you want to keep your monitoring history. Deleting it removes the local records created by the app.

## Exporting Data

After at least one check has been recorded, use the Download monitoring history (CSV) button from the dashboard.

The exported CSV file can be opened in Microsoft Excel, Google Sheets, or another spreadsheet application. It can also be used to prepare analysis tables or support the research report.

## Current Scope and Limitations

This is a local, manually triggered prototype.

- Checks run only when the user clicks Check now.
- The application does not perform background or scheduled monitoring.
- It does not currently send email, SMS, or push alerts.
- Monitoring records are stored only on the local computer.
- The app is not deployed in the cloud.
- Results depend on the user's internet connection, DNS resolution, remote website behaviour, and request timeout.
- A small number of checks over a short period cannot establish long-term website reliability.

These limitations should be stated clearly in demonstrations and any academic report or research paper.

## Future Improvements

Possible future extensions include:

1. Add scheduled monitoring at configurable intervals.
2. Run the monitoring worker continuously on a server or cloud platform.
3. Deploy the application on a suitable cloud service.
4. Store monitoring data in a managed database.
5. Send email alerts after repeated failures.
6. Add support for multiple users and grouped monitoring.
7. Compare monitoring intervals using detection delay and monitoring overhead.
8. Generate longer-term reports and downloadable performance summaries.

Cloud deployment and alerting are future enhancements and are not part of the current local prototype.

## Troubleshooting

### `python` is not recognised

On some Windows systems, use `py` instead:

```powershell
py --version
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

### `No module named streamlit`

Install the dependencies again using the Python launcher:

```powershell
py -m pip install -r requirements.txt
```

### Port 8501 is already in use

Run Streamlit on another port:

```powershell
py -m streamlit run app.py --server.port 8502
```

### A website is shown as Offline

Check that:

- The URL is correct.
- Your internet connection is working.
- The website can be reached from a normal browser.
- The website is not blocking automated requests.

A timeout or network restriction can cause a failed check even when the website works normally for other users.

## Responsible Use

Use this project for learning and for testing websites you are authorised to monitor. Keep the checking frequency reasonable and avoid overloading remote servers. Do not use the application to bypass access controls, disrupt services, or perform unauthorised monitoring.

For controlled downtime experiments, use a local test website or a server you own or have permission to test.

## Author

**Student Name:** [Karan Mahiya]

**Roll Number:** [590016816]

**Department / Batch:** [B.Tech. CSE / B-3 CCvT]

**Course:** Research Methodology

**Project:** Website Uptime Monitoring Dashboard

---

*Developed as an educational prototype using Python and open-source libraries.*
