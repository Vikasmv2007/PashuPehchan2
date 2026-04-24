-- ============================================================
-- Database: cattle_breed_db
-- Project: Image Based Breed Recognition for Cattle & Buffaloes
-- Ministry of Fisheries, Animal Husbandry & Dairying
-- ============================================================

CREATE DATABASE IF NOT EXISTS cattle_breed_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE cattle_breed_db;

-- ============================================================
-- Table: breeds
-- Stores reference data for Indian cattle and buffalo breeds
-- ============================================================
CREATE TABLE IF NOT EXISTS breeds (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    breed_name      VARCHAR(100)  NOT NULL,
    animal_type     ENUM('cattle', 'buffalo') NOT NULL,
    region          VARCHAR(150)  NOT NULL,
    milk_productivity VARCHAR(100) NOT NULL,
    traits          TEXT          NOT NULL,
    care_tips       TEXT          NOT NULL,
    economic_value  VARCHAR(200)  NOT NULL,
    image_url       VARCHAR(255)  DEFAULT NULL,
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Table: predictions
-- Stores uploaded image records and prediction results
-- ============================================================
CREATE TABLE IF NOT EXISTS predictions (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    image_path      VARCHAR(255)  NOT NULL,
    animal_type     ENUM('cattle', 'buffalo') NOT NULL,
    predicted_breed VARCHAR(100)  NOT NULL,
    confidence_score FLOAT        NOT NULL,
    location        VARCHAR(150)  DEFAULT NULL,
    age_years       FLOAT         DEFAULT NULL,
    notes           TEXT          DEFAULT NULL,
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Sample Data: Indian Cattle Breeds
-- ============================================================
INSERT INTO breeds (breed_name, animal_type, region, milk_productivity, traits, care_tips, economic_value) VALUES

('Gir', 'cattle',
 'Gujarat, Rajasthan, Maharashtra',
 '10–16 litres/day',
 'Prominent forehead, pendulous ears, deep red/yellow coat, long curved horns, large dewlap, well-adapted to tropical heat',
 'Provide shaded shelter during summer. Feed quality green fodder + dry roughage. Regular deworming every 3 months. Ideal stocking density: 2–3 animals per acre.',
 'Estimated ₹60,000–₹1,50,000 per animal. A2 milk fetches premium price. High export demand for semen and embryos globally.'),

('Sahiwal', 'cattle',
 'Punjab (Pakistan border region), Haryana, UP',
 '12–20 litres/day',
 'Reddish-brown coat, loose skin, short horns, calm temperament, high heat tolerance, excellent milk fat (5%)',
 'Requires high-energy diet during lactation. Avoid extreme cold – use jute covers in winter. Annual vaccination for FMD, BQ, HS. Provide mineral blocks.',
 'Estimated ₹80,000–₹2,00,000 per animal. Best A2 milk producer. Suited for crossbreeding programs.'),

('Red Sindhi', 'cattle',
 'Sindh region, Punjab, Rajasthan',
 '8–12 litres/day',
 'Deep red coat, short-stout build, medium size, tick-resistant skin, adapts well to poor feed conditions',
 'Can thrive on low-quality roughage. Supplement with mineral mix in dry seasons. Ideal for smallholder farmers with limited resources.',
 'Estimated ₹40,000–₹90,000 per animal. Highly valued in developing countries. Used in crossbreeding for tropical dairy.'),

('Tharparkar', 'cattle',
 'Rajasthan (Thar Desert), Gujarat',
 '8–10 litres/day',
 'White/grey coat, medium size, lyre-shaped horns, extremely drought-tolerant, long legs, efficient water metabolism',
 'Drought-adapted — minimal water requirements. Thrives on sparse desert vegetation. Protect from cold desert nights. Avoid waterlogged areas.',
 'Estimated ₹35,000–₹80,000 per animal. Excellent for arid zone dairy farming. Dual-purpose (milk + draft).'),

('Kankrej', 'cattle',
 'Kutch and Banaskantha (Gujarat)',
 '6–8 litres/day',
 'Silver/iron-grey coat, large lyre-shaped horns, massive body, very powerful draft animal, known for stamina',
 'Feed high-protein ration during work season. Hoof care important – trim regularly. Suitable for deep black-soil ploughing.',
 'Estimated ₹50,000–₹1,20,000 per animal. Premium draft breed. Strong demand in Gujarat for sugarcane farming.'),

('Ongole', 'cattle',
 'Andhra Pradesh (Guntur district)',
 '4–6 litres/day',
 'Large white/grey frame, pronounced hump, long pendulous ears, extreme heat tolerance, muscular build',
 'Excellent forager – low feed cost. Provide 40–50 litres water daily. Annual dipping for tick control. Ideal for low-input farming systems.',
 'Estimated ₹60,000–₹1,50,000 per animal. Global export to Brazil and USA as beef-dairy cross. Strong demand for draft.'),

('Hallikar', 'cattle',
 'Karnataka (Hassan, Tumkur)',
 '2–4 litres/day',
 'Sharp forward-pointing horns, compact build, light grey, highly energetic, fastest Indian draft breed, nimble on rocky terrain',
 'Needs ample exercise – avoid confined stalls. Feed jowar straw + green fodder. Used for fast cart-pulling; maintain hoof health.',
 'Estimated ₹40,000–₹80,000 per animal. Celebrated racing and draft breed of Karnataka. Cultural significance in Kambala races.'),

('Deoni', 'cattle',
 'Karnataka–Maharashtra border (Bidar, Latur)',
 '6–9 litres/day',
 'White body with black patches on face/legs (similar to Holstein coloring), medium size, dual-purpose, gentle nature',
 'Supplement with cotton seed cake during lactation. Regular FMD vaccination. Suitable for semi-arid Deccan plateau conditions.',
 'Estimated ₹35,000–₹75,000 per animal. Good dual-purpose breed for small farmers in Deccan region.');

-- ============================================================
-- Sample Data: Indian Buffalo Breeds
-- ============================================================
INSERT INTO breeds (breed_name, animal_type, region, milk_productivity, traits, care_tips, economic_value) VALUES

('Murrah', 'buffalo',
 'Haryana (Rohtak, Hisar), Punjab, Delhi',
 '15–25 litres/day',
 'Jet black body, tightly coiled (corkscrew) horns, bulky frame, high milk fat (7–8%), short legs, massive udder',
 'High-input breed – needs 15–18 kg green fodder + 4–5 kg concentrate daily. Regular bathing/wallowing essential. Keep cool in summer. Prone to mastitis – daily udder hygiene.',
 'Estimated ₹80,000–₹2,50,000 per animal. World-record milk producer among buffaloes. Premium ghee production.'),

('Surti', 'buffalo',
 'Gujarat (Surat, Vadodara, Kheda)',
 '8–12 litres/day',
 'Rust-brown/silver-black coat, two white chevron marks on neck, medium size, V-shaped horns, calm temperament',
 'Thrives in riverine/flood-prone areas. Feed paddy straw + groundnut cake. Excellent swimmer – do not confine near steep banks.',
 'Estimated ₹50,000–₹1,20,000 per animal. Popular in Gujarat dairy cooperatives (Amul network). Good butter fat content (8%).'),

('Jaffarabadi', 'buffalo',
 'Saurashtra region of Gujarat (Gir Forest area)',
 '10–15 litres/day',
 'Largest Indian buffalo breed, massive body (600–800 kg), heavy downward-curving horns, black skin, excellent milk fat',
 'Requires large space and heavy feed (20+ kg fodder). Regular mineral supplementation for bone health. Ideal for large-scale dairy farms.',
 'Estimated ₹1,00,000–₹3,00,000 per animal. Prestigious breed; stud bulls command high price. Premium paneer and khoa production.'),

('Nili-Ravi', 'buffalo',
 'Punjab (Ferozepur, Amritsar) – trans-border breed',
 '12–18 litres/day',
 'Black body, white markings on forehead/face/legs/tail tip, large size, wall-eye (blue iris), pendulous ears',
 'Feed nutrient-dense ration including mustard cake. Keep near water bodies for wallowing. Eye health monitoring important (white-eye trait).',
 'Estimated ₹75,000–₹2,00,000 per animal. Second-best milk producer after Murrah. Strong in Punjab cooperative dairies.'),

('Bhadawari', 'buffalo',
 'UP (Agra, Etawah), MP (Gwalior)',
 '5–7 litres/day',
 'Copper/brown tinge body, light-colored chevrons, small-medium size, extremely high milk fat (13%), drought-hardy',
 'Low-input breed – survives on coarse roughage. Supplement with linseed for coat health. Ideal for small marginal farmers.',
 'Estimated ₹40,000–₹90,000 per animal. Highest butterfat content of any buffalo (13%). Prized for pure desi ghee making.'),

('Nagpuri', 'buffalo',
 'Vidarbha region, Maharashtra',
 '6–9 litres/day',
 'Black body, white markings, long backward-curving horns, medium build, well-adapted to dry Deccan conditions',
 'Provide ample water during dry months (May–June). Neem leaf browse helps as natural dewormer. Good for orange-orchard farm integration.',
 'Estimated ₹45,000–₹1,00,000 per animal. Popular in Maharashtra rural dairies. Used for milk and draft in Vidarbha.');

-- ============================================================
-- Optional: View to join predictions with breed details
-- ============================================================
CREATE OR REPLACE VIEW prediction_summary AS
SELECT
    p.id,
    p.image_path,
    p.animal_type,
    p.predicted_breed,
    p.confidence_score,
    p.location,
    p.age_years,
    p.notes,
    p.created_at,
    b.region,
    b.milk_productivity,
    b.economic_value
FROM predictions p
LEFT JOIN breeds b
    ON p.predicted_breed = b.breed_name
    AND p.animal_type   = b.animal_type;
