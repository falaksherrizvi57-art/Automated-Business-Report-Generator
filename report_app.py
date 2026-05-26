import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Enterprise PDF Report Generator", page_icon="📊", layout="centered")

st.title("📊 Automated Business Report Engine")
st.write("Upload a raw CSV transactional file below to generate a publication-ready analytics summary report instantly.")

# --- STEP 1: EMBED SAMPLE DATA FOR TESTING ---
st.markdown("### 1. Download or View Sample Dataset Layout")
st.write("Your source file must contain these identical column labels: `Month`, `Revenue`, `Expenses`")

sample_data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'Revenue': [10000, 12500, 11000, 14000, 18000, 22500],
    'Expenses': [7000, 7500, 7200, 8000, 9500, 11000]
}
sample_df = pd.DataFrame(sample_data)
st.dataframe(sample_df)

# Provide a quick way to use sample data right inside the app
use_sample = st.checkbox("Use this sample data to test the generator engine")

# --- STEP 2: USER FILE UPLOAD SECTION ---
st.markdown("---")
st.markdown("### 2. Source File Upload")
uploaded_file = st.file_uploader("Choose your retail transaction CSV file:", type=["csv"])

# Define data source based on user choice
df = None
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("💾 Custom source file uploaded successfully!")
elif use_sample:
    df = sample_df.copy()
    st.info("ℹ️ Testing app pipeline utilizing baseline sample configurations.")

# --- STEP 3: DATA PROCESSING & CALCULATIONS ---
if df is not None:
    st.markdown("---")
    st.markdown("### 3. Data Integrity & Pipeline Analysis")
    
    # Calculate Profit metrics instantly
    df['Profit'] = df['Revenue'] - df['Expenses']
    
    # Display the processed computations live on screen
    st.dataframe(df)
    
    # Generate Totals
    total_rev = df['Revenue'].sum()
    total_exp = df['Expenses'].sum()
    total_profit = df['Profit'].sum()
    
    # Display professional interactive key performance summary cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Gross Aggregate Revenue", f"${total_rev:,}")
    col2.metric("Total Overhead Expenses", f"${total_exp:,}", delta=f"-${total_exp:,}", delta_color="inverse")
    col3.metric("Net Cleared Profit Yield", f"${total_profit:,}", delta=f"+${total_profit:,}")

    # --- STEP 4: TRIGGER RE-BUILDING THE SCRIPT ---
    if st.button("🚀 Compile and Generate Executive PDF Report"):
        with st.spinner("Processing calculations and formatting layout styles..."):
            
            # 1. Save an analytical plot image behind the scenes
            plt.figure(figsize=(6, 3.5))
            plt.plot(df['Month'], df['Revenue'], marker='o', color='#1f77b4', linewidth=2, label='Revenue')
            plt.bar(df['Month'], df['Profit'], color='#2ca02c', alpha=0.7, label='Net Profit')
            plt.title('Monthly Sales Performance Analysis', fontsize=12, fontweight='bold', pad=10)
            plt.xlabel('Month')
            plt.ylabel('Value ($)')
            plt.legend(loc='upper left')
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            plt.tight_layout()
            
            chart_filename = "temp_chart.png"
            plt.savefig(chart_filename, dpi=200)
            plt.close()
            
            # 2. Build the exact HTML layout matching our design standard
            table_rows_html = ""
            for index, row in df.iterrows():
                table_rows_html += f"""
                <tr>
                    <td style="font-weight: bold;">{row['Month']}</td>
                    <td style="text-align: right;">{row['Revenue']:,}.00</td>
                    <td style="text-align: right;">{row['Expenses']:,}.00</td>
                    <td style="text-align: right; font-weight: bold; color: #2F855A;">{row['Profit']:,}.00</td>
                </tr>
                """
                
            dynamic_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    @page {{ size: A4; margin: 20mm 15mm; }}
                    body {{ font-family: Arial, sans-serif; color: #2D3748; line-height: 1.6; }}
                    .banner {{ background: linear-gradient(135deg, #1A365D 0%, #2A4365 100%); color: white; padding: 20px; margin-bottom: 20px; }}
                    h2 {{ color: #1A365D; border-left: 4px solid #3182CE; padding-left: 10px; margin-top: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                    th {{ background-color: #EDF2F7; color: #1A365D; padding: 8px; text-align: left; border-bottom: 2px solid #CBD5E0; }}
                    td {{ padding: 8px; border-bottom: 1px solid #E2E8F0; }}
                    tr:nth-child(even) {{ background-color: #F7FAFC; }}
                </style>
            </head>
            <body>
                <div class="banner">
                    <h1 style="margin:0; font-size:20pt;">📊 Executive Performance Report</h1>
                    <p style="margin:5px 0 0 0; color:#E2E8F0; font-size:10pt;">Generated Dynamically via Python Automated Engine Pipeline</p>
                </div>
                <h2>1. Financial Summary Indicators</h2>
                <p>Gross Aggregated Revenue: <b>${total_rev:,}</b> | Cleared Yield Margin: <b>${total_profit:,}</b></p>
                
                <h2>2. Metrics Visualization Trend</h2>
                <div style="text-align:center;"><img src="{chart_filename}" width="450"/></div>
                
                <h2>3. Consolidated Transaction Ledger</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Month</th>
                            <th style="text-align: right;">Revenue ($)</th>
                            <th style="text-align: right;">Expenses ($)</th>
                            <th style="text-align: right;">Net Profit ($)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows_html}
                    </tbody>
                </table>
            </body>
            </html>
            """
            
            # --- FIXED AND CORRECTLY INDENTED HERE ---
            with open("temp_report.html", "w", encoding="utf-8") as f:
                f.write(dynamic_html)
                
            # Compile file into static distribution format using the background engine
            try:
                from weasyprint import HTML
                HTML("temp_report.html").write_pdf("Final_Generated_Report.pdf")
                
                # Provide real-time download capability directly to browser window
                with open("Final_Generated_Report.pdf", "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download Your Executive PDF Report",
                        data=pdf_file,
                        file_name="Executive_Performance_Report.pdf",
                        mime="application/pdf"
                    )
                st.success("✨ Your professional report has finished rendering! Click the download button above.")
            except Exception as e:
                st.error("Engine configuration check: Please ensure necessary document layout dependencies are installed.")
                st.info("To finish compiling on your local laptop, run: pip install weasyprint")