import matplotlib.pyplot as plt

def main():
    print("Welcome to the Student Expense Tracker!")

    try:
        # Input details
        income = float(input("Enter your total income: "))
        if income <= 0:
            raise ValueError("Income must be greater than 0.")

        tuition = float(input("Enter tuition expense: "))
        hostel = float(input("Enter hostel expense: "))
        food = float(input("Enter food expense: "))
        college_fee = float(input("Enter college fee expense: "))
        miscellaneous_expenses = float(input("Enter miscellaneous expenses: "))

        # Validate input values
        expenses = {
            "Tuition": validate_input("Tuition", tuition),
            "Hostel": validate_input("Hostel", hostel),
            "Food": validate_input("Food", food),
            "College Fee": validate_input("College Fee", college_fee),
            "Miscellaneous": validate_input("Miscellaneous", miscellaneous_expenses),
        }

        # Calculate total expenses and ratio
        total_expenses = sum(expenses.values())
        ratio = total_expenses / income

        # Display graph (Page 2)
        display_graph(expenses)

        # Display ratio and details (Page 3)
        print("\nIncome to Expense Ratio")
        print(f"Total Income: ${income:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Income-to-Expense Ratio: {ratio:.2f}")

        # Suggestions based on ratio (Page 4)
        if ratio > 0.7:
            print("\nSuggestions to Manage Expenses and Increase Income:")
            print("- Cut down on non-essential expenses.")
            print("- Explore part-time jobs or freelancing opportunities.")
            print("- Consider online tutoring or content creation.")
            print("- Reduce eating out or other luxury expenses.")
        elif ratio < 0.3:
            print("\nSuggestions to Save More:")
            print("- Invest your savings in a reliable investment plan.")
            print("- Open a high-yield savings account.")
            print("- Consider learning new skills to enhance your income potential.")
            print("- Set aside a fixed percentage of your income each month.")

        # Observations (Page 5)
        observations = input("\nNote down your observations or thoughts: ")
        print("\nThank you for using the Student Expense Tracker!")
        print(f"Your Notes: {observations}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please restart the program and provide valid inputs.")

def validate_input(name, value):
    if value < 0:
        raise ValueError(f"{name} expense cannot be negative.")
    return value

def display_graph(expenses):
    labels = list(expenses.keys())
    values = list(expenses.values())

    # Bar graph for expense breakdown
    plt.bar(labels, values, color=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'])
    plt.title('Monthly Expense Breakdown')
    plt.xlabel('Expense Categories')
    plt.ylabel('Amount ($)')
    plt.show()

if __name__ == "__main__":
    main()

