from typing import List, Optional
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from datetime import date
import db_helper  # Make sure this module has your DB functions

# --------------------------
# Initialize FastAPI app
# --------------------------
app = FastAPI(title="Expenses API")


# --------------------------
# Pydantic models
# --------------------------
class Expense(BaseModel):
    amount: float
    category: str
    notes: Optional[str] = None


class DateRange(BaseModel):
    start_date: date
    end_date: date


# --------------------------
# GET expenses for a date
# --------------------------
@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    """
    Fetch all expenses for a given date.
    Always returns a list of Expense objects, even if empty.
    """
    try:
        expenses = db_helper.fetch_expenses_for_date(expense_date)
        if not expenses:
            # Return empty list if no expenses found
            return []
        return expenses
    except Exception as e:
        # Log the error and return empty list instead of dict
        print(f"Error fetching expenses: {e}")
        return []


# --------------------------
# POST/Update expenses for a date
# --------------------------
@app.post("/expenses/{expense_date}")
def add_or_update_expense(
    expense_date: date,
    expenses: List[Expense] = Body(...)
):
    """
    Delete existing expenses for a date and insert new ones.
    """
    try:
        db_helper.delete_expenses_for_date(expense_date)
        for expense in expenses:
            db_helper.insert_expense(
                expense_date,
                expense.amount,
                expense.category,
                expense.notes
            )
        return {"message": f"{len(expenses)} expenses updated for {expense_date}"}
    except Exception as e:
        return {"error": str(e)}


# --------------------------
# POST analytics endpoint
# --------------------------
@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    """
    Get summarized analytics for the given date range.
    Automatically detects dict or tuple structure from DB and handles any column names.
    """
    data = db_helper.fetch_expense_summary(
        date_range.start_date,
        date_range.end_date
    )

    if not data:
        return {}

    breakdown = {}

    first_row = data[0]

    # Dict case
    if isinstance(first_row, dict):
        # Try to automatically find total and category keys
        total_key = next((k for k in first_row.keys() if 'total' in k.lower() or 'sum' in k.lower()), None)
        category_key = next((k for k in first_row.keys() if 'cat' in k.lower()), None)

        if not total_key or not category_key:
            raise HTTPException(status_code=500, detail="Unable to detect total/category keys in DB result")

        total = sum(row.get(total_key, 0) for row in data)

        for row in data:
            row_total = row.get(total_key, 0)
            category = row.get(category_key, 'Unknown')
            percentage = (row_total / total) * 100 if total != 0 else 0
            breakdown[category] = {"total": row_total, "percentage": round(percentage, 2)}

    # Tuple/list case
    else:
        # Assume first element is total, second is category
        total = sum(row[0] for row in data)
        for row in data:
            row_total = row[0]
            category = row[1] if len(row) > 1 else 'Unknown'
            percentage = (row_total / total) * 100 if total != 0 else 0
            breakdown[category] = {"total": row_total, "percentage": round(percentage, 2)}

    return breakdown
