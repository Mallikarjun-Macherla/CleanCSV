# CleanCSV

A simple, user-friendly web application for cleaning CSV files. Built with Python and Streamlit, this app helps you quickly remove duplicate rows, handle missing values, reset indices, and optionally remove outliers from numeric columns.

## Features
- Upload any CSV file
- Remove duplicate rows
- Drop rows with missing values
- Reset index after cleaning
- Remove outliers (choose columns and method: IQR or Z-score)
- Preview original and cleaned data (first 10 rows)
- Download the cleaned CSV file

## Getting Started

### Prerequisites
- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)
- [scipy](https://scipy.org/) (for Z-score outlier detection)

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Mallikarjun-Macherla/CleanCSV.git
   cd CleanCSV
   ```
2. Install dependencies:
   ```bash
   pip install streamlit pandas scipy
   ```

### Usage
1. Run the app:
   ```bash
   streamlit run app.py
   ```
2. Open the provided local URL in your browser.
3. Upload a CSV file and select your cleaning options.
4. Preview the results and download the cleaned file.

## Project Structure
```
├── app.py
├── sample_data.csv
├── README.md
└── .gitignore
```

## License
This project is licensed under the MIT License.

## Author
- [Mallikarjun Macherla](https://github.com/Mallikarjun-Macherla)

## Contact & Support
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/MallikarjunMacherla/)
- [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mallikarjunmac05@gmail.com)

