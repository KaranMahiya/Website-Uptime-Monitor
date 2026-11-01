import sqlite3
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

DB_NAME = "monitoring.db"
REQUEST_TIMEOUT = 10

st.set_page_config(
    page_title="Website Uptime Monitor",
    page_icon="🌐",
    layout="wide",
)

def normalize_url(raw_url: str) -> str:
    """Add HTTPS when a scheme is not supplied and validate the URL."""
    raw_url = raw_url.strip()
    if not raw_url:
        raise ValueError("Please enter a website URL.")
    if not raw_url.startswith(("http://", "https://")):
        raw_url = "https://" + raw_url
    parsed = urlparse(raw_url)
    if not parsed.netloc:
        raise ValueError("Enter a valid URL, such as https://example.com.")
    return raw_url

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS monitoring (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            response_time_ms REAL,
            status_code INTEGER,
            checked_at TEXT NOT NULL,
            error_message TEXT
        )
    """)
    conn.commit()
    return conn

def check_website(url: str):
    """Perform one HTTP GET check and return a record."""
    started = time.perf_counter()
    status = "Offline"
    status_code = None
    error_message = None
    response_time_ms = None

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
            headers={"User-Agent": "Student-Uptime-Monitor/1.0"},
        )
        response_time_ms = (time.perf_counter() - started) * 1000
        status_code = response.status_code
        status = "Online" if response.status_code < 400 else "Offline"
        if status == "Offline":
            error_message = f"HTTP {response.status_code}"
    except requests.RequestException as exc:
        response_time_ms = (time.perf_counter() - started) * 1000
        error_message = str(exc)[:250]

    return {
        "url": url,
        "status": status,
        "response_time_ms": response_time_ms,
        "status_code": status_code,
        "checked_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "error_message": error_message,
    }

def save_record(conn, record):
    conn.execute("""
        INSERT INTO monitoring
        (url, status, response_time_ms, status_code, checked_at, error_message)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        record["url"], record["status"], record["response_time_ms"],
        record["status_code"], record["checked_at"], record["error_message"]
    ))
    conn.commit()

def load_history(conn):
    return pd.read_sql_query(
        "SELECT * FROM monitoring ORDER BY id DESC", conn
    )

conn = get_connection()

st.title("🌐 Website Uptime Monitoring Dashboard")
st.caption("A student prototype for checking HTTP availability, response time, and historical uptime.")

with st.sidebar:
    st.header("Monitor a website")
    url_input = st.text_input("Website URL", placeholder="https://www.example.com")
    check_button = st.button("Check now", type="primary", width="stretch")
    st.divider()
    st.write("**How it works**")
    st.write("1. Send an HTTP request.")
    st.write("2. Record status and response time.")
    st.write("3. Save the result in a local SQLite database.")
    st.caption(f"Request timeout: {REQUEST_TIMEOUT} seconds")

if check_button:
    try:
        clean_url = normalize_url(url_input)
        with st.spinner(f"Checking {clean_url} ..."):
            result = check_website(clean_url)
            save_record(conn, result)
        if result["status"] == "Online":
            st.success(f"Website is ONLINE — HTTP {result['status_code']}")
        else:
            st.error(f"Website is OFFLINE / returned an error — {result['error_message'] or 'No response'}")
        if result["response_time_ms"] is not None:
            st.metric("Response time", f"{result['response_time_ms']:.2f} ms")
        st.info(f"Checked at: {result['checked_at']}")
    except ValueError as exc:
        st.warning(str(exc))

history = load_history(conn)

st.subheader("Latest monitoring records")
if history.empty:
    st.info("No checks have been recorded yet. Enter a URL in the sidebar and click **Check now**.")
else:
    # Summary is calculated for the most recently checked URL.
    latest_url = history.iloc[0]["url"]
    selected = history[history["url"] == latest_url]
    total = len(selected)
    successes = int((selected["status"] == "Online").sum())
    uptime = (successes / total * 100) if total else 0
    avg_response = selected["response_time_ms"].dropna().mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Latest website", latest_url)
    c2.metric("Checks recorded", total)
    c3.metric("Observed availability", f"{uptime:.1f}%")
    c4.metric("Average response", f"{avg_response:.1f} ms" if pd.notna(avg_response) else "N/A")

    st.caption("Availability is calculated from the checks stored for the latest website. It is not a certified service-level measurement.")
    st.dataframe(
        history[["url", "status", "status_code", "response_time_ms", "checked_at", "error_message"]],
        width="stretch",
        hide_index=True,
    )

    st.subheader("Response-time trend")
    chart_data = selected.copy()
    chart_data["checked_at"] = pd.to_datetime(chart_data["checked_at"], errors="coerce")
    chart_data = chart_data.dropna(subset=["checked_at", "response_time_ms"]).sort_values("checked_at")
    if not chart_data.empty:
        chart_data = chart_data.set_index("checked_at")
        st.line_chart(chart_data["response_time_ms"], y_label="Milliseconds")
    else:
        st.info("No response-time measurements are available for this website yet.")

    st.subheader("Availability by check")
    status_counts = selected["status"].value_counts().rename_axis("Status").reset_index(name="Checks")
    st.bar_chart(status_counts.set_index("Status"))

    csv_data = history.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download monitoring history (CSV)",
        data=csv_data,
        file_name="website_monitoring_history.csv",
        mime="text/csv",
    )

st.divider()
st.caption("Prototype note: this version checks a website when the user clicks the button. Continuous scheduled monitoring and email/SMS alerts are future enhancements.")
conn.close()
