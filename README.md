# Personal-finance-dashboard
A simple and effective personal financial tracker built with Streamlit and Python. It features a dashboard with charts, transaction history, and local data storage.

Features
Dashboard: A clear overview of your total income, expenses, deductions, and remaining balance.

Transaction Entry: An easy-to-use sidebar form for adding new transactions.

Data Persistence: Transactions are saved to a local JSON file (data.json) for persistence. Note: This will not persist on a hosted server. For a live app, you would need to use a database.

Visualizations: Interactive charts powered by Plotly to visualize your income vs. expenses and a breakdown of your spending by category.

Transaction History: Separate tables to view income, expense, and deduction transactions for easy filtering and review.

CSV Download: A button to download all your transaction data as a CSV file.

How to Run Locally
To get this app running on your local machine, follow these steps:

Clone the repository:

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd financial-tracker-app

Install the required packages:
Create a requirements.txt file in the project directory and install the dependencies.

pip install -r requirements.txt

Run the app:

streamlit run app.py

The app will open in your default web browser.

Deployment
This app can be easily deployed to the Streamlit Community Cloud.

Make sure your repository includes the app.py file and a requirements.txt file listing all the necessary libraries:

streamlit
pandas
plotly

Then, you can follow the instructions on the Streamlit Community Cloud platform to connect your GitHub repository and deploy the app.
