
# Expense Tracking System

A simple Expense Tracking System built with **FastAPI**, **MySQL**, **Python**, and **Streamlit**.  
This system provides APIs to track daily expenses, update them, and get summarized analytics over a date range with a friendly user interface.

---

## 🚀 Features

- Add or update expenses for a specific date.
- Fetch all expenses for a specific date.
- Get summarized expense analytics (total amount and percentage per category) for a date range.
- Interactive Streamlit frontend to manage expenses and view analytics.
- Persistent storage using MySQL database.

---

## 📦 Technologies Used

- **FastAPI** – Backend API framework.  
- **Streamlit** – Frontend interface for data input and analytics visualization.  
- **MySQL** – Database to store expense records.  
- **mysql-connector-python** – MySQL connector for Python.  
- **Pydantic** – Data validation models.  
- **Uvicorn** – ASGI server to run FastAPI.  
- **Requests** – For frontend-backend communication.  
- **Pandas** – For data manipulation and creating analytics tables.  
- **Pytest** – For testing your Python code.

---

## ⚙️ Installation Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/expense-tracking-system.git
    cd expense-tracking-system
    ```
2. Install dependencies:
    ```bash
    pip install fastapi mysql-connector-python pydantic uvicorn streamlit requests pandas pytest
    ```

3. Set up the MySQL database:
    ```sql
    CREATE DATABASE expense_manager;

    CREATE TABLE expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        expense_date DATE NOT NULL,
        amount FLOAT NOT NULL,
        category VARCHAR(255),
        notes TEXT
    );
    ```

4. Run the FastAPI backend:
    ```bash
    uvicorn server:app --reload
    ```

5. Run the Streamlit frontend:
    ```bash
    streamlit run app.py
    ```

---

## 🚪 API Endpoints

### ✅ 1. Get Expenses for a Date
- **GET** `/expenses/{expense_date}`
- Example:
    ```http
    GET http://127.0.0.1:8000/expenses/2024-08-01
    ```
- Response:
    ```json
    [
        {"amount": 200.0, "category": "Food", "notes": "Lunch"},
        {"amount": 50.0, "category": "Transport", "notes": "Bus fare"}
    ]
    ```

---

### ✅ 2. Add or Update Expenses for a Date
- **POST** `/expenses/{expense_date}`
- Body Example:
    ```json
    [
        {"amount": 100.0, "category": "Food", "notes": "Dinner"},
        {"amount": 20.0, "category": "Snacks", "notes": "Tea"}
    ]
    ```
- Response:
    ```json
    {"message": "2 expenses updated for 2024-08-01"}
    ```

---

### ✅ 3. Get Expense Analytics
- **POST** `/analytics/`
- Body Example:
    ```json
    {
        "start_date": "2024-08-01",
        "end_date": "2024-08-31"
    }
    ```
- Response Example:
    ```json
    {
        "Food": {"total": 500.0, "percentage": 62.5},
        "Transport": {"total": 300.0, "percentage": 37.5}
    }
    ```

---

## 🎨 Streamlit Frontend

- **Add/Update Tab**:  
  Interactive form to add or update expense records for a specific date.

- **Analytics Tab**:  
  Visual breakdown of expenses by category over a selected date range with bar chart and table.

---

## ⚠️ Troubleshooting

- Ensure MySQL service is running on `localhost:3306`.
- Use `127.0.0.1` instead of `localhost` in the connection parameters to avoid socket issues.
- Test DB connection manually:
    ```bash
    mysql -h 127.0.0.1 -P 3306 -u root -p
    ```
- Check firewall settings to allow port `3306`.

---

## 🎯 Future Improvements

- Add user authentication system.
- Implement Docker for easier deployment.
- Add more detailed expense categories and reports.

---

## 📄 License

MIT License – Feel free to use and modify.
