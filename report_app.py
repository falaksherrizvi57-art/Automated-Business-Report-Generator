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
    
    # Define the columns our engine absolutely requires
    required_columns = ['Month', 'Revenue', 'Expenses']
    
    # Check if all required columns exist in the uploaded file
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        # Gracefully handle the wrong file format instead of crashing!
        st.error(f"⚠️ **Invalid File Structure Detected!**")
        st.write(f"Your uploaded file is missing these required columns: `{', '.join(missing_columns)}`")
        st.info(f"Your file currently has these columns: `{', '.join(df.columns.tolist())}`. Please check the sample dataset layout in Step 1 and upload a compatible file.")
    else:
        # If everything looks perfect, proceed with calculations smoothly
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
                
                # 1. Adjusted chart dimensions and font sizes for crisp scaling
                plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
                fig, ax = plt.subplots(figsize=(6, 3))
                
                ax.plot(df['Month'], df['Revenue'], marker='o', color='#1A365D', linewidth=2.5, label='Revenue')
                ax.bar(df['Month'], df['Profit'], color='#2F855A', alpha=0.8, label='Net Profit', width=0.4)
                
                ax.set_title('Monthly Financial Trend Analysis', fontsize=11, fontweight='bold', color='#1A365D', pad=12)
                ax.set_xlabel('Reporting Month', fontsize=9, color='#4A5568')
                ax.set_ylabel('Amount ($)', fontsize=9, color='#4A5568')
                ax.tick_params(axis='both', labelsize=8)
                ax.legend(loc='upper left', fontsize=8, frameon=True)
                ax.grid(True, axis='y', linestyle='--', alpha=0.6)
                
                plt.tight_layout()
                
                chart_filename = "temp_chart.png"
                plt.savefig(chart_filename, dpi=300)
                plt.close()
                
                # 2. Build table rows dynamically
                table_rows_html = ""
                for index, row in df.iterrows():
                    table_rows_html += f"""
                    <tr>
                        <td style="font-weight: 600; color: #2D3748; padding: 10px 12px;">{row['Month']}</td>
                        <td style="text-align: right; padding: 10px 12px;">${row['Revenue']:,}.00</td>
                        <td style="text-align: right; padding: 10px 12px; color: #9B2C2C;">${row['Expenses']:,}.00</td>
                        <td style="text-align: right; font-weight: bold; color: #2F855A; padding: 10px 12px;">${row['Profit']:,}.00</td>
                    </tr>
                    """
                    
                # 3. Premium corporate document template structure
                dynamic_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        @page {{ size: A4; margin: 25mm 20mm 20mm 20mm; }}
                        body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #2D3748; line-height: 1.6; font-size: 10pt; }}
                        .header-container {{ border-bottom: 2px solid #1A365D; padding-bottom: 8px; margin-bottom: 25px; }}
                        .report-title {{ color: #1A365D; font-size: 22pt; font-weight: bold; margin: 0 0 5px 0; letter-spacing: -0.5px; }}
                        .report-subtitle {{ color: #718096; font-size: 10pt; margin: 0; text-transform: uppercase; letter-spacing: 1px; }}
                        .meta-table {{ width: 100%; margin-bottom: 25px; font-size: 9pt; color: #4A5568; }}
                        h2 {{ color: #1A365D; font-size: 13pt; font-weight: bold; margin-top: 25px; margin-bottom: 12px; border-bottom: 1px solid #E2E8F0; padding-bottom: 5px; }}
                        p {{ margin-bottom: 15px; color: #4A5568; }}
                        .chart-wrapper {{ text-align: center; margin: 20px 0; padding: 10px; border: 1px solid #E2E8F0; background-color: #F7FAFC; border-radius: 4px; }}
                        .chart-img {{ width: 100%; max-width: 480px; height: auto; }}
                        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 9.5pt; }}
                        th {{ background-color: #1A365D; color: white; padding: 10px 12px; text-align: left; font-weight: 600; }}
                        td {{ border-bottom: 1px solid #E2E8F0; }}
                        tr:nth-child(even) td {{ background-color: #F7FAFC; }}
                        .total-row td {{ background-color: #EDF2F7 !important; border-top: 2px solid #1A365D; border-bottom: 2px solid #1A365D; font-weight: bold; color: #1A365D; }}
                    </style>
                </head>
                <body>
                    <div class="header-container">
                        <h1 class="report-title">Executive Performance Report</h1>
                        <p class="report-subtitle">Corporate Operational Analytics & Intelligence</p>
                    </div>
                    <table class="meta-table">
                        <tr><td><strong>Prepared For:</strong> Retail Operations Portfolio</td><td style="text-align: right;"><strong>Date:</strong> May 2026</td></tr>
                        <tr><td><strong>Analysis Pipeline:</strong> Automated Data Engine</td><td style="text-align: right;"><strong>Status:</strong> Final Distribution</td></tr>
                    </table>
                    <h2>1. Financial Summary Indicators</h2>
                    <p>This automated document compiles multi-channel transactional records processed through our standard analytics script. Top-line generated revenue reached an aggregate of <b>${total_rev:,}.00</b>, yielding a net corporate cleared profit of <b>${total_profit:,}.00</b> after accounting for all baseline operating overhead allocations.</p>
                    <h2>2. Metrics Visualization Trend</h2>
                    <div class="chart-wrapper"><img class="chart-img" src="{chart_filename}"/></div>
                    <h2>3. Consolidated Transaction Ledger</h2>
                    <table>
                        <thead>
                            <tr><th>Reporting Month</th><th style="text-align: right;">Revenue ($)</th><th style="text-align: right;">Expenses ($)</th><th style="text-align: right;">Net Profit ($)</th></tr>
                        </thead>
                        <tbody>
                            {table_rows_html}
                            <tr class="total-row">
                                <td style="padding: 12px;">Total H1 Summary</td>
                                <td style="text-align: right; padding: 12px;">${total_rev:,}.00</td>
                                <td style="text-align: right; padding: 12px; color: #9B2C2C;">${total_exp:,}.00</td>
                                <td style="text-align: right; padding: 12px; color: #2F855A;">${total_profit:,}.00</td>
                            </tr>
                        </tbody>
                    </table>
                </body>
                </html>
                """
                
                # Fixed indentation and standard character maps
                with open("temp_report.html", "w", encoding="utf-8") as f:
                    f.write(dynamic_html)
                    
                try:
                    from weasyprint import HTML
                    HTML("temp_report.html").write_pdf("Final_Generated_Report.pdf")
                    
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
