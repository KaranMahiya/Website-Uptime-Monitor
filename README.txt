# Website Uptime Monitor

## Run
1. Open this folder in VS Code.
2. In the terminal, run:
   `py -m pip install requests streamlit pandas matplotlib`
3. Run:
   `py -m streamlit run app.py`
4. In the browser sidebar, enter a URL such as `https://www.wikipedia.org` and click **Check now**.

## Files
- `app.py`: Streamlit dashboard and HTTP checker.
- `monitoring.db`: created automatically when the app runs; stores check history.
- `research_paper.docx`: editable research-paper draft.

## Important scope note
This is a working prototype with user-triggered checks. It does not yet run unattended checks every 10/30/60 seconds or send email/SMS alerts. Those should only be described as implemented if you add and test them. The research paper includes a results table template; replace it with your own measured results.
