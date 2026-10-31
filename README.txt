# 🌐 Website Uptime Monitoring Dashboard

A lightweight Python application for checking whether a website is reachable, measuring its HTTP response time, and keeping a history of monitoring checks in a local SQLite database.

The project uses **Streamlit** to provide a simple browser-based dashboard. It was developed as a student project for learning about website availability monitoring, HTTP requests, data storage, and basic performance analysis.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [How It Works](#how-it-works)
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

Website availability is important for online services such as educational portals, e-commerce websites, and information systems. If a website becomes unavailable or responds slowly, users may be unable to access the service.

This project provides a basic monitoring dashboard that allows a user to:

1. Enter a website URL.
2. Send an HTTP GET request to that website.
3. check the returned HTTP status code.
4. Measure the time taken for the request to complete.
5. Save the result with a timestamp.
6. Review previous checks and response-time trends.

The application is intended as an educational prototype. It currently performs checks when the user clicks **Check now**; it is not an unattended, continuously running monitoring service.

## Features

- **Website availability check** — checks an HTTP/HTTPS URL.
- **HTTP status code** — displays the response status code, such as `200`.
- **Response-time measurement** — records elapsed request time in milliseconds.
- **Online/offline classification** — treats HTTP status codes below `400` as Online; status codes of `400` or higher and request failures are classified as Offline.
- **Monitoring history** — stores each check in a local SQLite database.
- **Observed availability** — calculates the percentage of successful checks in the saved records for the latest website.
- **Response-time chart** — visualises recorded response-time measurements.
- **CSV export** — downloads the monitoring history for further analysis.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Interactive web dashboard |
| Requests | Sends HTTP requests to websites |
| SQLite | Stores monitoring records locally |
| Pandas | Reads and organises monitoring data |
| Matplotlib | Supports data visualisation |

## How It Works

```text
        User enters a website URL
                    |
                    v
          Streamlit dashboard
                    |
                    v
          Python monitoring logic
                    |
                    v
          HTTP GET request (Requests)
                    |
          +---------+---------+
          |                   |
          v                   v
     HTTP response       Request error
          |                   |
          v                   v
  Read status code      Record failure
  Measure elapsed time
          |                   |
          +---------+---------+
                    |
                    v
          Save result in SQLite
                    |
                    v
       Dashboard, history and charts
                    |
                    v
              CSV download
```

## Project Structure

Website_Uptime_Monitor/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation
├── monitoring.db               # Created automatically when the app runs
└── Research_Paper_Draft.docx   # Research paper draft (if included)
```

`monitoring.db` is generated automatically in the working directory when the application creates its database. It may not exist until the first run.

## Requirements

- Windows 10 or Windows 11 (instructions below use Windows).
- Python 3.10 or later.
- Visual Studio Code or another Python editor.
- An internet connection to check public websites.
- A modern web browser.

The project does not require paid cloud services or special hardware for local execution.

## Installation

### 1. Download or extract the project

Extract the project ZIP file, if you downloaded it as a ZIP archive.

### 2. Open the project in VS Code

1. Open Visual Studio Code.
2. Select **File → Open Folder**.
3. Choose the `Website_Uptime_Monitor` folder.
4. Open **Terminal → New Terminal**.

### 3. Check Python

In the terminal, run:

```powershell
py --version
```

If Python is installed, the terminal should display a version number, for example:

```text
Python 3.14.10
```

If the `py` command is unavailable, install Python from [python.org](https://www.python.org/downloads/) and select **Add Python to PATH** during installation.

### 4. Install dependencies

Run:

```powershell
py -m pip install -r requirements.txt
```

If you do not have `requirements.txt`, install the packages directly:

```powershell
py -m pip install streamlit requests pandas matplotlib
```

Wait for the installation to finish.

## Run the Application

From the project folder, run:

```powershell
py -m streamlit run app.py
```

Streamlit will start a local web server and normally open the dashboard in your default browser.

If the browser does not open automatically, copy the **Local URL** shown in the terminal (usually `http://localhost:8501`) and open it manually.

To stop the application, return to the terminal and press:

```text
Ctrl + C
```

## How to Use

1. Start the application using the command above.
2. In the left sidebar, find **Monitor a website**.
3. Enter a URL.
4. Click **Check now**.
5. Read the status message, HTTP status code, and response time.
6. Review the monitoring history and charts on the main page.
7. Repeat checks to collect more observations.
8. Use **Download monitoring history (CSV)** to save the records.

Enter the complete URL when possible, including `https://`. The application adds `https://` if no HTTP/HTTPS scheme is supplied.

## Understanding the Results

### Website status

- **Online:** the website returned an HTTP status code below `400`.
- **Offline:** the request failed, timed out, or returned an HTTP status code of `400` or higher.

This is a simplified classification. Some websites may return an error status even though their server is reachable.

### HTTP status code

An HTTP status code describes the result of the request. For example:

- `200` — OK; the request succeeded.
- `301` or `302` — redirect.
- `403` — forbidden.
- `404` — not found.
- `500` — internal server error.

Requests follows redirects by default in this project, so the recorded status code is generally the final response code.

### Response time

Response time is measured by the client application and shown in milliseconds (`ms`). It is the elapsed time for the HTTP request to complete, not a direct measurement of server processing time alone.

### Observed availability

The dashboard calculates:

```text
Observed availability (%) =
(Number of successful checks / Total checks) × 100
```

For example, if 9 out of 10 checks are successful:

```text
Observed availability = (9 / 10) × 100 = 90%
```

This percentage describes only the checks stored in the local database. It is not a guarantee of long-term uptime or a formal service-level agreement (SLA).

## Database

The application uses **SQLite**, a lightweight database included with Python.

The database file is named:

```text
monitoring.db
```

Each check stores:

- Website URL
- Status (`Online` or `Offline`)
- Response time in milliseconds
- HTTP status code
- Date and time of the check
- Error message, if a request failed

Do not delete `monitoring.db` if you want to keep your monitoring history. Deleting it removes the locally stored records.

## Exporting Data

After at least one check has been recorded, use the dashboard's **Download monitoring history (CSV)** button.

The CSV file can be opened in Microsoft Excel, Google Sheets, or another spreadsheet application. It can also be used to calculate averages and prepare tables for the research report.

## Current Scope and Limitations

The current version is a local, manually triggered prototype.

- Checks run only when the user clicks **Check now**.
- The application does not currently run scheduled checks in the background.
- It does not currently send email, SMS, or push notifications.
- Monitoring records are stored on the local computer.
- The application is not currently deployed on AWS or another cloud platform.
- Results depend on the user's internet connection, DNS resolution, remote website behaviour, and request timeout.
- A small number of checks over a short period cannot establish long-term website reliability.

These limitations should be stated accurately in demonstrations and the research paper.

## Future Improvements

Possible extensions include:

1. Add scheduled monitoring at configurable intervals.
2. Run the monitoring worker continuously on a server or cloud platform.
3. Deploy the application using an appropriate AWS service.
4. Store monitoring data in a managed cloud database.
5. Send email alerts after repeated failures.
6. Add multiple user accounts and monitor groups of websites.
7. Compare monitoring intervals using detection delay and monitoring overhead.
8. Add longer-term reports and downloadable performance summaries.

Cloud deployment and alerting are future enhancements, not features of the current local prototype.

## Troubleshooting

### `python` is not recognised

On some Windows installations, use `py` instead:

```powershell
py --version
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

### `No module named streamlit` (or another package)

Install the dependencies again using the same Python launcher:

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
- The website is reachable in a normal browser.
- The website is not blocking automated requests.

A request timeout or network restriction can cause a failed check even when the website works for other users.

## Responsible Use

Use the tool for learning and for checking websites you are authorised to monitor. Keep the checking frequency reasonable. Do not use the application to overload websites, bypass access controls, or disrupt services. For controlled downtime experiments, use a local test website or a server that you own or have permission to test.

## Author

**Student Name:** ______________________________  
**Roll Number:** _______________________________  
**Department / College:** ______________________  
**Course:** Research Methodology  
**Project:** Website Uptime Monitoring Dashboard

---

*Developed as an educational prototype using Python and open-source libraries.*
