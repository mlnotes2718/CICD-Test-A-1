from flask import Flask, jsonify, request, render_template

app = Flask(__name__, static_folder="static")


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if height_m <= 0:
        raise ValueError("Height must be greater than zero")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero")
    return weight_kg / (height_m * height_m)


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obesity"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/bmi", methods=['GET', 'POST'])
def bmi_api():
    weight_kg = request.form.get("weight_kg")
    height_m = request.form.get("height_m")

    try:
        weight = float(weight_kg)
        height = float(height_m)
        bmi = calculate_bmi(weight, height)
    except (TypeError, ValueError):
        return jsonify({"error": "Please provide valid numeric values for weight_kg and height_m."}), 400

    return render_template("result.html", bmi=round(bmi, 2), category=bmi_category(bmi))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
