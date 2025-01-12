from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Email configuration
SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "your_password"
RECIPIENT_EMAIL = "recipient@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587

@app.route('/')
def home():
    return "Welcome to the Form Submission App!"

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.form

    # Extract form fields
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Construct the email content
    subject = "New Form Submission"
    body = f"""
    You have received a new form submission:
    
    Name: {name}
    Email: {email}
    Message: {message}
    """

    # Send email
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return jsonify({"message": "Form submitted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
