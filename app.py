from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb+srv://eedevnsskjayanthasa:Sravanasandhya@jayanth.uxkld.mongodb.net/")
db = client['renu_biome_db']
collection = db['product_orders']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/order', methods=['GET'])
def get_order_by_phone():
    phone = request.args.get('phone', '').strip()
    if not phone:
        return jsonify({"message": "Phone number not provided"}), 400

    order = collection.find_one({ "phone": phone })
    if not order:
        return jsonify({"message": "No order found"}), 404

    return jsonify({
        "name": order.get("name"),
        "email": order.get("email"),
        "address": order.get("address", "N/A"),
        "products": order.get("products", []),
        "number_of_products": order.get("number_of_products", []),
        "calculated_price": order.get("calculated_price"),
    })

@app.route('/api/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    recipient = data['email']
    subject = "Order Confirmation - Renu Biome"
    body = f"""Hello {data["name"]},

Thank you for your order!

Details:
- Product(s): {", ".join(data["products"])}
- Quantity: {", ".join(data["number_of_products"])}
- Price: {data["calculated_price"]} $
- Payment Method: {data["payment_method"]}

We will process your order shortly.

Regards,
Renu Biome Team
"""

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = "managerasasolutions@gmail.com"
        msg['To'] = recipient

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("managerasasolutions@gmail.com", "mqhwdbeplthtgdlp")
            smtp.send_message(msg)

        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        return jsonify({"message": "Failed to send email", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
