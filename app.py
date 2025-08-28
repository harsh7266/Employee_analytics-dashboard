import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO

st.set_page_config(page_title='Employee Analytics', layout='wide', initial_sidebar_state='expanded')

@st.cache_data
def load_data(path='data/employees.csv'):
    df = pd.read_csv(path)
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    return df

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

def simple_insights(df):
    insights = []
    if 'Department' in df.columns:
        avg_by_dept = df.groupby('Department')['PerformanceScore'].mean().sort_values(ascending=False)
        best = avg_by_dept.index[0]
        insights.append(f"Top performing department (avg score): {best} ({avg_by_dept.iloc[0]:.2f})")
    if 'Salary' in df.columns:
        high = df['Salary'].mean()
        insights.append(f"Average salary across company: ₹{high:,.0f}")
    # Example comparative insight
    if 'Department' in df.columns and 'Salary' in df.columns and 'PerformanceScore' in df.columns:
        dept_stats = df.groupby('Department').agg({'Salary':'mean','PerformanceScore':'mean'})
        if len(dept_stats) >= 2:
            top_salary_dept = dept_stats['Salary'].idxmax()
            top_perf_dept = dept_stats['PerformanceScore'].idxmax()
            insights.append(f"Department with highest avg salary: {top_salary_dept}")
            if top_salary_dept != top_perf_dept:
                insights.append(f"Note: Highest paid dept ({top_salary_dept}) is not the top performing dept ({top_perf_dept}).") 
    return insights


df = load_data()

st.title('📈 Advanced Employee Analytics Dashboard')
st.markdown('Interactive HR analytics with filtering, search, export and automated insights.')

# Sidebar filters
st.sidebar.header('Filters & Actions')
departments = st.sidebar.multiselect('Department', options=sorted(df['Department'].unique()), default=sorted(df['Department'].unique()))
min_salary, max_salary = int(df['Salary'].min()), int(df['Salary'].max())
salary_range = st.sidebar.slider('Salary range', min_salary, max_salary, (min_salary, max_salary))
perf_min, perf_max = int(df['PerformanceScore'].min()), int(df['PerformanceScore'].max())
perf_range = st.sidebar.slider('Performance score range', perf_min, perf_max, (perf_min, perf_max))
year_min, year_max = int(df['YearJoined'].min()), int(df['YearJoined'].max())
year_range = st.sidebar.slider('Year Joined', year_min, year_max, (year_min, year_max))
search_name = st.sidebar.text_input('Search by name')

st.sidebar.markdown('---')
if st.sidebar.button('Export filtered to Excel'):
    filtered = df[(df['Department'].isin(departments)) & 
                  (df['Salary'].between(salary_range[0], salary_range[1])) &
                  (df['PerformanceScore'].between(perf_range[0], perf_range[1])) &
                  (df['YearJoined'].between(year_range[0], year_range[1]))]
    data_xlsx = to_excel(filtered)
    st.sidebar.download_button('Download Excel', data_xlsx, file_name='employee_filtered.xlsx')

# Filter dataframe
df_filtered = df[(df['Department'].isin(departments)) & 
                 (df['Salary'].between(salary_range[0], salary_range[1])) &
                 (df['PerformanceScore'].between(perf_range[0], perf_range[1])) &
                 (df['YearJoined'].between(year_range[0], year_range[1]))]

if search_name:
    df_filtered = df_filtered[df_filtered['Name'].str.contains(search_name, case=False, na=False)]

# KPIs
total_emp = len(df_filtered)
avg_salary = df_filtered['Salary'].mean() if total_emp>0 else 0
avg_perf = df_filtered['PerformanceScore'].mean() if total_emp>0 else 0

k1, k2, k3 = st.columns(3)
k1.metric('Total Employees', total_emp)
k2.metric('Average Salary', f'₹{avg_salary:,.0f}')
k3.metric('Average Performance', f'{avg_perf:.2f}')

# Automated insights
st.subheader('Automated Insights')
for ins in simple_insights(df_filtered):
    st.info(ins)

# Tabs for visuals and table
tab1, tab2 = st.tabs(['Visuals', 'Data Table'])

with tab1:
    col1, col2 = st.columns([2,1])
    with col1:
        # Salary by department (box)
        fig_salary = px.box(df_filtered, x='Department', y='Salary', title='Salary Distribution by Department', points='all')
        st.plotly_chart(fig_salary, use_container_width=True)

        # Performance heatmap (department vs year)
        pivot = df_filtered.pivot_table(index='Department', columns='YearJoined', values='PerformanceScore', aggfunc='mean')
        if pivot.shape[0]>0 and pivot.shape[1]>0:
            fig_heat = px.imshow(pivot, text_auto=True, title='Avg Performance (Dept vs Year)')
            st.plotly_chart(fig_heat, use_container_width=True)

    with col2:
        fig_dept = px.histogram(df_filtered, x='Department', title='Employees by Department')
        st.plotly_chart(fig_dept, use_container_width=True)

        fig_perf = px.histogram(df_filtered, x='PerformanceScore', nbins=5, title='Performance Score Distribution')
        st.plotly_chart(fig_perf, use_container_width=True)

with tab2:
    st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

st.caption('Built with Streamlit — upgradeable for deployment to Streamlit Cloud or Heroku.')
