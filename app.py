from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Member model
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    plan = db.Column(db.String(20), nullable=False)
    want_trainer = db.Column(db.Boolean, nullable=False)
    payment_status = db.Column(db.String(10), nullable=False)
    join_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    trainer_id = db.Column(db.Integer, nullable=True)  # Optional

# Create tables
with app.app_context():
    db.create_all()
    print("✅ Database and tables created!")

# Add member route
@app.route('/add_member', methods=['POST'])
def add_member():
    data = request.get_json()

    try:
        # Required fields
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        phone_number = data.get('phoneNumber')
        age = data.get('age')
        gender = data.get('gender')
        plan = data.get('plan')
        want_trainer = data.get('wantTrainer')
        payment_status = data.get('paymentStatus')
        join_date = datetime.strptime(data.get('joinDate'), "%Y-%m-%d").date()
        end_date = datetime.strptime(data.get('endDate'), "%Y-%m-%d").date()
        trainer_id = data.get('trainerId') if want_trainer else None

        if not all([first_name, last_name, phone_number, age, gender, plan, payment_status, join_date, end_date]):
            return jsonify({"error": "Missing required fields"}), 400

        new_member = Member(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            age=age,
            gender=gender,
            plan=plan,
            want_trainer=want_trainer,
            payment_status=payment_status,
            join_date=join_date,
            end_date=end_date,
            trainer_id=trainer_id
        )

        db.session.add(new_member)
        db.session.commit()

        return jsonify({"message": "Member added successfully"}), 201

    except Exception as e:
        print("❌ Error adding member:", e)
        return jsonify({"error": "Failed to add member"}), 500

# Run app
if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(debug=True)
