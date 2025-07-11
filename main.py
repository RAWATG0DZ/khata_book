from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

CSV_URL = "https://docs.google.com/spreadsheets/d/1NXamPzzIwOyNYwYLg3GPSxLw51Euijjy1LydQiK46vE/export?format=csv"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ayush Khata Book</title>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f4f4f4; }
        table { border-collapse: collapse; width: 100%; background: white; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #eee; }
        h1 { color: #2c3e50; }
    </style>
</head>
<body>
    <h1>📘 Ayush Khata Book</h1>
    {{ table|safe }}
    {% if total %}
        <h2>🧮 Total Baki: ₹{{ total }}</h2>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def khata():
    try:
        df = pd.read_csv(CSV_URL)
        df.columns = [c.lower().strip() for c in df.columns]
        total = None
        if 'qty' in df.columns and 'rate' in df.columns:
            df['amount'] = df['qty'] * df['rate']
            total = df['amount'].sum()
        table_html = df.to_html(index=False)
        return render_template_string(HTML_TEMPLATE, table=table_html, total=total)
    except Exception as e:
        return f"<h3>Error: {e}</h3>"

if __name__ == '__main__':
    app.run()
