# PashuPehchan — AI Breed Recognition for Indian Cattle & Buffaloes
**Smart India Hackathon 2024**  
**Organization:** Ministry of Fisheries, Animal Husbandry & Dairying  
**Theme:** Agriculture, FoodTech & Rural Development

---

## Folder Structure

```
cattle_breed_app/
├── app.py                  ← Flask application (routes, prediction logic)
├── schema.sql              ← MySQL database schema + sample breed data
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
│
├── templates/
│   ├── base.html           ← Base layout (navbar, footer, flash messages)
│   ├── index.html          ← Home / landing page
│   ├── upload.html         ← Image upload & prediction results page
│   ├── breeds.html         ← Breed library (cattle & buffalo)
│   └── records.html        ← Admin records view
│
└── static/
    ├── css/
    │   └── style.css       ← All styles (no Bootstrap)
    └── uploads/            ← Uploaded animal images stored here
```

---

## Quick Setup

### 1. Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- pip

### 2. Install Dependencies

```bash
cd cattle_breed_app
pip install -r requirements.txt
```

### 3. Set Up MySQL Database

Open MySQL shell and run:

```sql
-- Create and populate database
SOURCE path/to/cattle_breed_app/schema.sql;
```

Or run directly from terminal:

```bash
mysql -u root -p < schema.sql
```

### 4. Configure Database Credentials

Edit `app.py` lines 34–39:

```python
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",           # ← Your MySQL username
    "password": "your_password",  # ← Your MySQL password
    "database": "cattle_breed_db",
    "autocommit": True,
}
```

### 5. Run the Application

```bash
python app.py
```

Visit: **http://localhost:5000**

---

## Pages

| Route       | Description                              |
|-------------|------------------------------------------|
| `/`         | Home page — hero, features, team         |
| `/upload`   | Upload animal photo & get breed result   |
| `/breeds`   | Breed encyclopedia (cattle & buffalo)    |
| `/records`  | Admin panel — all submitted records      |

---

## Sample MySQL Commands

```sql
-- View all records
USE cattle_breed_db;
SELECT * FROM predictions ORDER BY created_at DESC;

-- Count by animal type
SELECT animal_type, COUNT(*) as total FROM predictions GROUP BY animal_type;

-- View all cattle breeds
SELECT breed_name, region, milk_productivity FROM breeds WHERE animal_type='cattle';

-- Top predicted breeds
SELECT predicted_breed, COUNT(*) as count
FROM predictions
GROUP BY predicted_breed
ORDER BY count DESC;

-- Average confidence per breed
SELECT predicted_breed, AVG(confidence_score)*100 as avg_conf
FROM predictions
GROUP BY predicted_breed
ORDER BY avg_conf DESC;
```

---

## Connecting Your CNN Model

In `app.py`, find the `predict_breed()` function (around line 90).  
Replace the dummy logic with your trained model:

```python
# Example with TensorFlow/Keras:
import tensorflow as tf
import numpy as np
from PIL import Image

MODEL = tf.keras.models.load_model('models/breed_cnn.h5')
CATTLE_LABELS = ['Deoni', 'Gir', 'Hallikar', 'Kankrej', 'Ongole',
                 'Red Sindhi', 'Sahiwal', 'Tharparkar']
BUFFALO_LABELS = ['Bhadawari', 'Jaffarabadi', 'Murrah',
                  'Nagpuri', 'Nili-Ravi', 'Surti']

def predict_breed(image_path: str, animal_type: str) -> dict:
    img = Image.open(image_path).resize((224, 224))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, 0)
    probs = MODEL.predict(arr)[0]
    labels = CATTLE_LABELS if animal_type == 'cattle' else BUFFALO_LABELS
    idx = int(np.argmax(probs))
    return {
        "breed": labels[idx],
        "confidence": float(probs[idx]),
        # ... fetch rest from DB using breed name
    }
```

---

## Tech Stack

- **Frontend:** HTML5, CSS3 (custom, no Bootstrap)
- **Backend:** Python 3, Flask
- **Database:** MySQL
- **Fonts:** Playfair Display + DM Sans (Google Fonts)
- **AI Model:** CNN (placeholder — integrate your trained model)

---

## Team

| Name          | Role                  |
|---------------|-----------------------|
| Priya Sharma  | ML Engineer           |
| Arjun Mehta   | Backend Developer     |
| Sneha Patil   | UI/UX Designer        |
| Rohit Yadav   | Domain Expert         |
