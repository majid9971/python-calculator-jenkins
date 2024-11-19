from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/calculate', methods=['GET'])
def calculate():
    num1 = request.args.get('num1')
    num2 = request.args.get('num2')
    operation = request.args.get('operation')
    
    if not num1 or not num2 or not operation:
        return jsonify({"error": "All parameters (num1, num2, operation) are required"}), 400

    try:
        num1 = float(num1)
        num2 = float(num2)
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                return jsonify({"error": "Division by zero is not allowed"}), 400
            result = num1 / num2
        else:
            return jsonify({"error": "Invalid operation"}), 400
        
        return jsonify({"result": result})

    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
