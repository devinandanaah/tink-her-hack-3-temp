from flask import Flask, render_template
from flask import request
from flask_cors import CORS
import matplotlib.pyplot as plt
import io
import base64
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# HTML Template
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Expense Tracker</title>
</head>
<body>
    <h1>Welcome to the Student Expense Tracker!</h1>
    <form method="POST" action="/">
        <label>Are you a Hosteller or Day Scholar?</label><br>
        <input type="radio" name="student_type" value="Hosteller" required> Hosteller<br>
        <input type="radio" name="student_type" value="Day Scholar" required> Day Scholar<br><br>
        <label>Total Income: </label><input type="number" step="0.01" name="income" required><br>
        <label>Tuition Expense: </label><input type="number" step="0.01" name="tuition" required><br>
        <label id="travel_or_hostel_label">Hostel Expense: </label><input type="number" step="0.01" name="hostel_or_travel" required><br>
        <label>Food Expense: </label><input type="number" step="0.01" name="food" required><br>
        <label>College Fee: </label><input type="number" step="0.01" name="college_fee" required><br>
        <label>Miscellaneous Expenses: </label><input type="number" step="0.01" name="miscellaneous" required><br>
        <label>Domain of Interest: </label><input type="text" name="domain" placeholder="e.g., Technology, Arts" required><br>
        <button type="submit">Submit</button>
    </form>
    {% if results %}
        <h2>Income to Expense Ratio</h2>
        <p>Total Income: ${{ results['income'] }}</p>
        <p>Total Expenses: ${{ results['total_expenses'] }}</p>
        <p>Income-to-Expense Ratio: {{ results['ratio'] }}</p>

        {% if results['suggestions'] %}
            <h2>Suggestions</h2>
            <ul>
                {% for suggestion in results['suggestions'] %}
                    <li>{{ suggestion }}</li>
                {% endfor %}
            </ul>
        {% endif %}

        {% if results['side_hustles'] %}
            <h2>Suggested Side Hustles</h2>
            <ul>
                {% for hustle in results['side_hustles'] %}
                    <li>{{ hustle }}</li>
                {% endfor %}
            </ul>
        {% endif %}

        <h2>Expense Breakdown</h2>
        <img src="data:image/png;base64,{{ results['graph'] }}" alt="Expense Breakdown">
    {% endif %}
</body>
</html>
"""

# Generate Expense Graph
def generate_graph(expenses):
    labels = list(expenses.keys())
    values = list(expenses.values())

    plt.bar(labels, values, color=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'])
    plt.title('Monthly Expense Breakdown')
    plt.xlabel('Expense Categories')
    plt.ylabel('Amount ($)')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    return graph_url

# Suggestions for Side Hustles
def get_side_hustles(domain):
    domain_hustles = {
        "Technology": [
            "Freelance web development - https://www.freecodecamp.org/",
            "Create and sell software tools - https://www.udemy.com/course/python-for-beginners-learn-programming-from-scratch/",
            "Online tutoring in programming - https://www.coursera.org/"
        ],
        "Arts": [
            "Sell art on Etsy - https://www.etsy.com/",
            "Create and sell digital designs - https://www.canva.com/",
            "Offer art classes online - https://www.skillshare.com/"
        ],
        "Finance": [
            "Start a personal finance blog - https://www.wordpress.com/",
            "Offer bookkeeping services - https://www.quickbooks.intuit.com/",
            "Investing tutorials - https://www.investopedia.com/"
        ]
    }
    return domain_hustles.get(domain, ["Explore freelancing opportunities in your area of interest."])

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None

    if request.method == 'POST':
    

        try:
            data = request.form
            student_type = data['student_type']
            income = float(data['income'])
            tuition = float(data['tuition'])
            hostel_or_travel = float(data['hostel_or_travel'])
            food = float(data['food'])
            college_fee = float(data['college_fee'])
            miscellaneous = float(data['miscellaneous'])
            domain = data['domain']

            if student_type == "Hosteller":
                expenses = {
                    "Tuition": validate_input("Tuition", tuition),
                    "Hostel": validate_input("Hostel", hostel_or_travel),
                    "Food": validate_input("Food", food),
                    "College Fee": validate_input("College Fee", college_fee),
                    "Miscellaneous": validate_input("Miscellaneous", miscellaneous),
                }
            else:
                expenses = {
                    "Tuition": validate_input("Tuition", tuition),
                    "Travel": validate_input("Travel", hostel_or_travel),
                    "Food": validate_input("Food", food),
                    "College Fee": validate_input("College Fee", college_fee),
                    "Miscellaneous": validate_input("Miscellaneous", miscellaneous),
                }

            total_expenses = sum(expenses.values())
            ratio = total_expenses / income

            suggestions = []
            if total_expenses > income:
                suggestions = [
                    "Explore part-time jobs or freelancing opportunities.",
                    "Cut down on non-essential expenses.",
                    "Consider online tutoring or content creation.",
                    "Reduce eating out or other luxury expenses."
                ]
            elif total_expenses < income:
                suggestions = [
                    "Invest your savings in a reliable investment plan.",
                    "Open a high-yield savings account.",
                    "Set aside a fixed percentage of your income each month.",
                    "Consider learning new skills to enhance your income potential."
                ]

            side_hustles = get_side_hustles(domain)

            graph = generate_graph(expenses)

            results = {
                "income": f"{income:.2f}",
                "total_expenses": f"{total_expenses:.2f}",
                "ratio": f"{ratio:.2f}",
                "suggestions": suggestions,
                "side_hustles": side_hustles,
                "graph": graph
            }

        except ValueError as e:
            results = {"error": str(e)}
    return render_template('index.html', results=results)

# Validate Input
def validate_input(name, value):
    if value < 0:
        raise ValueError(f"{name} expense cannot be negative.")
    return value

if __name__ == '__main__':
    app.run(debug=True)
