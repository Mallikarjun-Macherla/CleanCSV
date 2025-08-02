import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="CSV Cleaner", layout="centered")
st.title("CSV Cleaner Web App")

st.markdown("""
Upload a CSV file to clean duplicates and missing values, preview the results, and download the cleaned file.
""")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])


# Main screen cleaning options
st.markdown("## Cleaning Options")
col1, col2, col3 = st.columns(3)
with col1:
    remove_duplicates = st.checkbox("Remove duplicate rows", value=True)
with col2:
    drop_missing = st.checkbox("Drop rows with missing values", value=True)
with col3:
    reset_index = st.checkbox("Reset index after cleaning", value=True)


# Read CSV only once and reuse
df_original = None
numeric_cols = []
if uploaded_file:
    try:
        df_original = pd.read_csv(uploaded_file)
        numeric_cols = df_original.select_dtypes(include='number').columns.tolist()
    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty or not a valid CSV. Please upload a valid CSV file.")
    except pd.errors.ParserError:
        st.error("There was a problem parsing the CSV file. Please check the file format and try again.")

# Outlier removal options
remove_outliers = st.checkbox("Remove outliers (numeric columns)", value=False)
outlier_cols = []
outlier_method = ""
if df_original is not None and remove_outliers and numeric_cols:
    st.markdown("**Select columns for outlier removal:**")
    outlier_cols = st.multiselect("Columns:", numeric_cols, default=numeric_cols)
    outlier_method = st.radio("Outlier detection method:", ["IQR", "Z-score"], index=0)

if df_original is not None:
    st.success("CSV file uploaded successfully!")
    st.markdown("---")
    st.markdown("### Data Preview")
    st.write("**Original Data (first 10 rows):**")
    st.dataframe(df_original.head(10), use_container_width=True)

    clean_btn = st.button("Clean", type="primary")
    if clean_btn:
        df_cleaned = df_original.copy()
        report = []
        dup_removed = 0
        na_removed = 0
        outliers_removed = 0

        # Apply selected cleaning steps
        if remove_duplicates:
            rows_before = len(df_cleaned)
            df_cleaned = df_cleaned.drop_duplicates()
            dup_removed = rows_before - len(df_cleaned)
            report.append(f"- Duplicate rows removed: {dup_removed}")
        else:
            report.append("- Duplicate rows not removed.")

        if drop_missing:
            rows_before_na = len(df_cleaned)
            df_cleaned = df_cleaned.dropna()
            na_removed = rows_before_na - len(df_cleaned)
            report.append(f"- Rows with missing values removed: {na_removed}")
        else:
            report.append("- Rows with missing values not removed.")

        # Remove outliers
        if remove_outliers and outlier_cols:
            rows_before_out = len(df_cleaned)
            if outlier_method == "IQR":
                for col in outlier_cols:
                    Q1 = df_cleaned[col].quantile(0.25)
                    Q3 = df_cleaned[col].quantile(0.75)
                    IQR = Q3 - Q1
                    df_cleaned = df_cleaned[(df_cleaned[col] >= Q1 - 1.5 * IQR) & (df_cleaned[col] <= Q3 + 1.5 * IQR)]
            elif outlier_method == "Z-score":
                from scipy.stats import zscore
                zscores = df_cleaned[outlier_cols].apply(zscore)
                mask = (zscores.abs() < 3).all(axis=1)
                df_cleaned = df_cleaned[mask]
            outliers_removed = rows_before_out - len(df_cleaned)
            report.append(f"- Outliers removed: {outliers_removed} (method: {outlier_method}, columns: {', '.join(outlier_cols)})")
        elif remove_outliers:
            report.append("- Outlier removal selected, but no columns chosen.")
        else:
            report.append("- Outliers not removed.")

        if reset_index:
            df_cleaned = df_cleaned.reset_index(drop=True)
            report.append("- Index reset after cleaning.")
        else:
            report.append("- Index not reset.")

        st.markdown("---")
        st.markdown("### Cleaning Report")
        for line in report:
            st.write(line)

        st.markdown("---")
        st.markdown("### Cleaned Data Preview")
        st.write("**Cleaned Data (first 10 rows):**")
        st.dataframe(df_cleaned.head(10), use_container_width=True)

        st.markdown("---")
        st.markdown("### Download Cleaned CSV")
        csv_buffer = io.StringIO()
        df_cleaned.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download cleaned_data.csv",
            data=csv_buffer.getvalue(),
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload a CSV file to begin.")

# Footer with clickable author link (no icon)
st.markdown("---")
st.markdown('<div style="text-align:center; font-size:16px;">Made by <a href="https://github.com/Mallikarjun-Macherla" target="_blank">Mallikarjun Macherla</a></div>', unsafe_allow_html=True)
