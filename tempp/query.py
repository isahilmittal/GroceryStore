from flask import Flask, jsonify, request
from sql_connection import sql_connection
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
import base64

app = Flask(__name__)

def get_available_months():
    connection = sql_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT DATE_FORMAT(date_time, '%m-%y') AS month FROM orders ORDER BY month")
    months = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return months


def get_monthly_data(month):
    connection = sql_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        month, year = month.split("-")
        month = int(month)
        year = int("20" + str(year))
    except ValueError:
        return {"error": "Invalid month format. Expected format: MM-YYYY"}

    query = """
        SELECT SUM(amount) AS total_revenue 
        FROM orders 
        WHERE MONTH(date_time) = %s AND YEAR(date_time) = %s 
    """
    cursor.execute(query, (month, year))
    total_revenue = cursor.fetchone()["total_revenue"] or 0

    query = """
        SELECT DATE(date_time) AS dated, SUM(amount) AS total, COUNT(order_id) AS order_count
        FROM orders 
        WHERE MONTH(date_time) = %s AND YEAR(date_time) = %s
        GROUP BY dated
        ORDER BY dated
    """
    cursor.execute(query, (month, year))
    daily_revenue = cursor.fetchall()
    cursor.close()
    connection.close()

    df = pd.DataFrame(daily_revenue)
    if not df.empty:
        df["dated"] = pd.to_datetime(df["dated"]).dt.strftime("%a, %d %b")  # Formatting date
        df["order_count"] = df["order_count"].astype(int)
        df["total"] = df["total"].astype(float)

    return {
        "total_revenue": total_revenue,
        "daily_revenue": df.to_dict(orient='records'),
    }

def generate_chart_image(df, chart_type):
    img = io.BytesIO()
    
    if chart_type in ["bar", "line"]:
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")

        if chart_type == "bar":
            sns.barplot(x=df["dated"], y=df["total"], color="royalblue", edgecolor="black")
            plt.legend(["Total Revenue"], loc="upper left")

        elif chart_type == "line":
            sns.lineplot(x=df["dated"], y=df["total"], marker="o", color="red", linewidth=2.5)
            plt.legend(["Total Revenue"], loc="upper left")

        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Revenue (₹)")
        plt.title("Daily Revenue Trend")
        plt.tight_layout()
        
        plt.savefig(img, format="png", bbox_inches="tight")
        plt.close()

    elif chart_type == "pie":
        df["date_label"] = df["dated"].dt.strftime("%a, %d %b")  # Format dates
        fig = px.pie(df, values="total", names="date_label", title="Revenue Distribution", color_discrete_sequence=px.colors.qualitative.Pastel)
        img.write(fig.to_image(format="png"))

    img.seek(0)
    encoded_img = base64.b64encode(img.getvalue()).decode()
    
    return encoded_img