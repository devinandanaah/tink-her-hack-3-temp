
function toggleExpenseField() {
    const studentType = document.querySelector('input[name="student_type"]:checked').value;
    const label = document.getElementById("dynamic_label");
    const input = document.getElementById("dynamic_input");

    if (studentType === "Hosteller") {
        label.textContent = "Hostel Expense:";
        input.placeholder = "Enter hostel expense";
    } else {
        label.textContent = "Travel Expense:";
        input.placeholder = "Enter travel expense";
    }
}
window.onload = function() {
    toggleExpenseField();
};
