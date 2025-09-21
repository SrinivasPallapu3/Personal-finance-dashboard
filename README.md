# Personal Finance Dashboard

A simple and effective **personal financial tracker** built with **Streamlit** and **Python**. It features a dashboard with interactive charts, transaction history, and local data storage for easy tracking of your income, expenses, and deductions.

---

## 🌟 Features

- **Dashboard:** A clear overview of your total **income**, **expenses**, **deductions**, and **remaining balance**.
- **Transaction Entry:** An easy-to-use **sidebar form** for adding new transactions.
- **Data Persistence:** Transactions are saved to a local **JSON file (`data.json`)** for persistence.
  - *Note:* This will **not persist on a hosted server**. For a live app, you will need to use a proper **database**.
- **Visualizations:** Interactive charts powered by **Plotly** to visualize:
  - Income vs. Expenses
  - Spending breakdown by category
- **Transaction History:** Separate tables for **income**, **expenses**, and **deductions** for easy filtering and review.
- **CSV Download:** Export your transaction data as a **CSV file** with one click.

---

## 🛠️ How to Run Locally

Follow these steps to run the app on your local machine:

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd financial-tracker-app
```

### 2. Install the required packages:

Create a `requirements.txt` file in your project directory with the following contents:

```txt
streamlit
pandas
plotly
```

Then, install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the app:

```bash
streamlit run app.py
```

The app will automatically open in your default web browser.

---

## 📄 Example `requirements.txt`

```txt
streamlit
pandas
plotly
```
---

## 🔗 Links
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/)
