# ============================================================
# app.py — Main Flask Application
# Project: Image Based Breed Recognition for Cattle & Buffaloes
# Organization: Ministry of Fisheries, Animal Husbandry & Dairying
# ============================================================

import os
import random
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import Error

# ─────────────────────────────────────────────
# App Configuration
# ─────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "cattle_breed_hackathon_2024"

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB max upload

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ─────────────────────────────────────────────
# MySQL Connection
# Update these credentials to match your setup
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",           # ← Change to your MySQL username
    "password": "your_password",  # ← Change to your MySQL password
    "database": "cattle_breed_db",
    "autocommit": True,
}


def get_db_connection():
    """Return a live MySQL connection, or None on failure."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None


# ─────────────────────────────────────────────
# Dummy Prediction Engine
# ─────────────────────────────────────────────
# TODO: Replace this function with your trained CNN model.
# Expected interface:
#   predict_breed(image_path: str, animal_type: str) -> dict
#     Returns: { "breed": str, "confidence": float 0-1,
#                "description": str, "care_tips": str,
#                "economic_value": str, "region": str,
#                "milk_productivity": str }

CATTLE_BREEDS = [
    {"breed": "Gir", "confidence": 0.94, "region": "Gujarat, Rajasthan",
     "milk_productivity": "10–16 litres/day",
     "description": "The Gir is one of India's premier dairy breeds, originating from the Gir Forest of Gujarat. Distinguished by its prominent dome-shaped forehead and long pendulous ears, it is well-adapted to tropical heat and produces high-quality A2 milk rich in beta-casein protein.",
     "care_tips": "Provide shaded shelter in summer. Feed quality green fodder + dry roughage. Deworm every 3 months. Vaccinate against FMD and BQ annually.",
     "economic_value": "₹60,000–₹1,50,000 per animal. A2 milk commands premium market price. Global demand for semen and embryos."},
    {"breed": "Sahiwal", "confidence": 0.89, "region": "Punjab, Haryana",
     "milk_productivity": "12–20 litres/day",
     "description": "Sahiwal is India's highest milk-producing indigenous breed, prized for its A2 milk with 5% fat content. Its calm temperament and heat tolerance make it ideal for smallholder dairy farming across North India.",
     "care_tips": "High-energy diet during lactation. Provide jute covers in winter. Annual FMD, BQ, and HS vaccination. Keep mineral blocks available.",
     "economic_value": "₹80,000–₹2,00,000 per animal. Best indigenous dairy breed for crossbreeding programs."},
    {"breed": "Tharparkar", "confidence": 0.82, "region": "Rajasthan, Gujarat",
     "milk_productivity": "8–10 litres/day",
     "description": "The Tharparkar is a dual-purpose breed from the Thar Desert, uniquely adapted to arid conditions with minimal water needs. Its efficient metabolism allows it to thrive on sparse desert vegetation.",
     "care_tips": "Minimal water requirements. Thrives on desert vegetation. Protect from cold desert nights. Avoid waterlogged areas.",
     "economic_value": "₹35,000–₹80,000 per animal. Excellent for arid zone dairy and draft work."},
    {"breed": "Ongole", "confidence": 0.78, "region": "Andhra Pradesh",
     "milk_productivity": "4–6 litres/day",
     "description": "The Ongole is a large, powerful Zebu breed from coastal Andhra Pradesh, globally recognised for beef-dairy crossbreeding. Its massive hump and extreme heat tolerance make it a draft powerhouse.",
     "care_tips": "Excellent forager – low feed cost. Provide 40–50 litres water daily. Annual tick dipping. Ideal for low-input farming.",
     "economic_value": "₹60,000–₹1,50,000 per animal. High export demand in Brazil and USA for crossbreeding."},
    {"breed": "Kankrej", "confidence": 0.85, "region": "Gujarat (Kutch, Banaskantha)",
     "milk_productivity": "6–8 litres/day",
     "description": "The Kankrej is a majestic silver-grey breed known for its lyre-shaped horns and exceptional strength. Highly prized as a draft animal for black-cotton soil ploughing in Gujarat.",
     "care_tips": "High-protein ration during work season. Regular hoof trimming. Suitable for heavy ploughing tasks.",
     "economic_value": "₹50,000–₹1,20,000 per animal. Premium draft breed with strong demand in sugarcane farming."},
]

BUFFALO_BREEDS = [
    {"breed": "Murrah", "confidence": 0.96, "region": "Haryana, Punjab",
     "milk_productivity": "15–25 litres/day",
     "description": "The Murrah is the world's most productive buffalo breed and the backbone of India's dairy industry. Its tightly coiled (corkscrew) horns and jet-black coat are hallmark features. Milk has 7–8% fat, ideal for ghee and paneer production.",
     "care_tips": "Needs 15–18 kg green fodder + 4–5 kg concentrate daily. Daily bathing essential. Keep cool in summer. Daily udder hygiene to prevent mastitis.",
     "economic_value": "₹80,000–₹2,50,000 per animal. World-record milk producer. Premium source for ghee."},
    {"breed": "Surti", "confidence": 0.87, "region": "Gujarat (Surat, Vadodara)",
     "milk_productivity": "8–12 litres/day",
     "description": "The Surti buffalo is distinguished by its two characteristic white chevron marks on the neck and a rust-brown coat. It thrives in riverine areas and is the backbone of Gujarat's Amul cooperative dairy network.",
     "care_tips": "Feed paddy straw + groundnut cake. Excellent swimmer. Do not confine near steep river banks.",
     "economic_value": "₹50,000–₹1,20,000 per animal. Popular in Gujarat dairy cooperatives. 8% butterfat content."},
    {"breed": "Jaffarabadi", "confidence": 0.91, "region": "Gujarat (Saurashtra)",
     "milk_productivity": "10–15 litres/day",
     "description": "The Jaffarabadi is the largest Indian buffalo breed, weighing 600–800 kg, with heavy downward-curving horns. Originating from Saurashtra near the Gir Forest, it is a prestige breed for large-scale dairy operations.",
     "care_tips": "Requires large space and 20+ kg fodder daily. Regular mineral supplementation for bone health.",
     "economic_value": "₹1,00,000–₹3,00,000 per animal. Stud bulls command premium prices. Ideal for paneer and khoa production."},
    {"breed": "Bhadawari", "confidence": 0.80, "region": "UP (Agra, Etawah), MP",
     "milk_productivity": "5–7 litres/day",
     "description": "The Bhadawari is a small, hardy buffalo with the highest butterfat content (13%) of any buffalo breed in the world — making its milk exceptionally valuable for desi ghee. A drought-resilient breed ideal for marginal farmers.",
     "care_tips": "Low-input breed – survives on coarse roughage. Supplement with linseed for coat health.",
     "economic_value": "₹40,000–₹90,000 per animal. Highest butterfat (13%) — prized for pure desi ghee."},
    {"breed": "Nili-Ravi", "confidence": 0.88, "region": "Punjab (Ferozepur, Amritsar)",
     "milk_productivity": "12–18 litres/day",
     "description": "The Nili-Ravi is a large, high-performing buffalo from Punjab identified by its distinctive white wall-eye (blue iris) and white markings on the face and legs. It is the second-best milk producer after the Murrah.",
     "care_tips": "Feed mustard cake supplements. Keep near water for wallowing. Monitor eye health regularly.",
     "economic_value": "₹75,000–₹2,00,000 per animal. Second-best milk producer. Strong in Punjab cooperative dairies."},
]


def predict_breed(image_path: str, animal_type: str) -> dict:
    """
    Dummy prediction function — returns realistic sample breed data.

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    TODO: Replace this with your trained CNN model.
    Suggested integration:
        import tensorflow as tf  # or torch
        model = tf.keras.models.load_model('models/breed_cnn.h5')
        img = preprocess_image(image_path)
        probs = model.predict(img)
        breed_idx = np.argmax(probs)
        return {"breed": BREED_LABELS[breed_idx],
                "confidence": float(probs[0][breed_idx]), ...}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    pool = CATTLE_BREEDS if animal_type == "cattle" else BUFFALO_BREEDS
    result = random.choice(pool)
    # Randomize confidence slightly for demo realism
    result = dict(result)
    result["confidence"] = round(
        min(0.99, result["confidence"] + random.uniform(-0.05, 0.05)), 2
    )
    return result


# ─────────────────────────────────────────────
# Utility
# ─────────────────────────────────────────────
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route("/")
def home():
    """Landing page with hero, features, and team sections."""
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Image upload and breed prediction page."""
    result = None
    form_data = {}

    if request.method == "POST":
        animal_type = request.form.get("animal_type", "cattle")
        location    = request.form.get("location", "")
        age         = request.form.get("age", None)
        notes       = request.form.get("notes", "")

        form_data = {
            "animal_type": animal_type,
            "location": location,
            "age": age,
            "notes": notes,
        }

        # Validate file
        if "image" not in request.files or request.files["image"].filename == "":
            flash("Please select an image file to upload.", "error")
            return render_template("upload.html", result=None, form_data=form_data)

        file = request.files["image"]
        if not allowed_file(file.filename):
            flash("Unsupported file type. Please upload JPG, PNG, or WEBP.", "error")
            return render_template("upload.html", result=None, form_data=form_data)

        # Save file with unique name
        ext = file.filename.rsplit(".", 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
        file.save(save_path)

        # Run prediction
        prediction = predict_breed(save_path, animal_type)
        result = {
            "image_path":   unique_name,
            "breed":        prediction["breed"],
            "confidence":   prediction["confidence"],
            "description":  prediction["description"],
            "care_tips":    prediction["care_tips"],
            "economic_value": prediction["economic_value"],
            "region":       prediction["region"],
            "milk_productivity": prediction["milk_productivity"],
            "animal_type":  animal_type,
            "location":     location,
        }

        # Persist to database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO predictions
                       (image_path, animal_type, predicted_breed, confidence_score,
                        location, age_years, notes)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                        unique_name,
                        animal_type,
                        prediction["breed"],
                        prediction["confidence"],
                        location,
                        float(age) if age else None,
                        notes,
                    ),
                )
                conn.close()
            except Error as e:
                print(f"[DB INSERT ERROR] {e}")
        else:
            flash("Database unavailable — result shown but not saved.", "warning")

    return render_template("upload.html", result=result, form_data=form_data)


@app.route("/breeds")
def breeds():
    """Breed encyclopedia page — reads from DB or falls back to static data."""
    cattle_list  = []
    buffalo_list = []

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM breeds WHERE animal_type='cattle' ORDER BY breed_name"
            )
            cattle_list = cursor.fetchall()
            cursor.execute(
                "SELECT * FROM breeds WHERE animal_type='buffalo' ORDER BY breed_name"
            )
            buffalo_list = cursor.fetchall()
            conn.close()
        except Error as e:
            print(f"[DB READ ERROR] {e}")
    else:
        # Fallback static data so the page always renders during development
        cattle_list = [
            {"breed_name": "Gir", "region": "Gujarat, Rajasthan", "milk_productivity": "10–16 L/day",
             "traits": "Prominent dome-shaped forehead, pendulous ears, deep red coat, curved horns",
             "economic_value": "₹60,000–₹1,50,000"},
            {"breed_name": "Sahiwal", "region": "Punjab, Haryana", "milk_productivity": "12–20 L/day",
             "traits": "Reddish-brown coat, loose skin, short horns, calm temperament",
             "economic_value": "₹80,000–₹2,00,000"},
            {"breed_name": "Tharparkar", "region": "Rajasthan, Gujarat", "milk_productivity": "8–10 L/day",
             "traits": "White/grey coat, lyre-shaped horns, drought-tolerant, long legs",
             "economic_value": "₹35,000–₹80,000"},
            {"breed_name": "Ongole", "region": "Andhra Pradesh", "milk_productivity": "4–6 L/day",
             "traits": "Large white/grey frame, pronounced hump, extreme heat tolerance",
             "economic_value": "₹60,000–₹1,50,000"},
            {"breed_name": "Kankrej", "region": "Gujarat", "milk_productivity": "6–8 L/day",
             "traits": "Silver-grey coat, lyre-shaped horns, powerful draft animal",
             "economic_value": "₹50,000–₹1,20,000"},
            {"breed_name": "Hallikar", "region": "Karnataka", "milk_productivity": "2–4 L/day",
             "traits": "Sharp forward-pointing horns, light grey, fastest Indian draft breed",
             "economic_value": "₹40,000–₹80,000"},
        ]
        buffalo_list = [
            {"breed_name": "Murrah", "region": "Haryana, Punjab", "milk_productivity": "15–25 L/day",
             "traits": "Jet black, corkscrew horns, massive udder, 7–8% milk fat",
             "economic_value": "₹80,000–₹2,50,000"},
            {"breed_name": "Surti", "region": "Gujarat", "milk_productivity": "8–12 L/day",
             "traits": "Two white chevron marks on neck, rust-brown coat, V-shaped horns",
             "economic_value": "₹50,000–₹1,20,000"},
            {"breed_name": "Jaffarabadi", "region": "Gujarat (Saurashtra)", "milk_productivity": "10–15 L/day",
             "traits": "Largest Indian buffalo (600–800 kg), heavy curved horns",
             "economic_value": "₹1,00,000–₹3,00,000"},
            {"breed_name": "Bhadawari", "region": "UP, MP", "milk_productivity": "5–7 L/day",
             "traits": "Copper-brown tinge, highest butterfat (13%), drought-hardy, small build",
             "economic_value": "₹40,000–₹90,000"},
            {"breed_name": "Nili-Ravi", "region": "Punjab", "milk_productivity": "12–18 L/day",
             "traits": "Black body, white markings, distinctive wall-eye (blue iris)",
             "economic_value": "₹75,000–₹2,00,000"},
        ]

    return render_template("breeds.html", cattle_list=cattle_list, buffalo_list=buffalo_list)


@app.route("/records")
def records():
    """Admin page — displays all prediction records from database."""
    all_records = []
    total = 0
    cattle_count = 0
    buffalo_count = 0
    avg_confidence = 0.0

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM predictions ORDER BY created_at DESC"
            )
            all_records = cursor.fetchall()

            total = len(all_records)
            cattle_count  = sum(1 for r in all_records if r["animal_type"] == "cattle")
            buffalo_count = sum(1 for r in all_records if r["animal_type"] == "buffalo")
            if total:
                avg_confidence = round(
                    sum(r["confidence_score"] for r in all_records) / total * 100, 1
                )
            conn.close()
        except Error as e:
            print(f"[DB READ ERROR] {e}")
            flash("Could not load records from the database.", "error")
    else:
        flash("Database connection failed. Showing empty records view.", "error")

    return render_template(
        "records.html",
        records=all_records,
        total=total,
        cattle_count=cattle_count,
        buffalo_count=buffalo_count,
        avg_confidence=avg_confidence,
    )


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
