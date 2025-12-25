from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "NETWEHUB backend работает!"})

@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})


@app.route("/ei-score", methods=["POST"])
def ei_score():
    data = request.get_json()
    # допустим, в data приходит список чисел, просто складываем
    answers = data.get("answers", [])
    score = sum(answers)
    return jsonify({"ei_score": score})


if __name__ == "__main__":
    app.run(debug=True)
