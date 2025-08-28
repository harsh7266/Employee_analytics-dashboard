# Advanced Employee Analytics Dashboard (Streamlit)

## Features
- Interactive filters for Department, Salary range, Performance score, and Year joined
- Employee search by name
- KPI cards for quick metrics
- Automated insights (simple comparative analytics)
- Visuals: Salary box plots, department histogram, performance heatmap
- Export filtered data to Excel

## Run locally
1. Create virtual env (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # mac/linux
   venv\\Scripts\\activate # windows
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. The app will open at `http://localhost:8501`

## Notes
- To deploy: push to GitHub and deploy on Streamlit Community Cloud or other hosting.
