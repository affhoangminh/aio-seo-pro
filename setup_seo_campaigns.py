
import sqlite3
import json
from datetime import datetime

def setup_campaigns():
    db_path = 'database/profiles.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    campaigns = [
        {
            "name": "01. Brand & Trust",
            "time": "08:00",
            "scripts": [
                {"path": "scripts/seo_brand_authority.json", "delay": 5},
                {"path": "scripts/seo_local_trust.json", "delay": 0}
            ]
        },
        {
            "name": "02. Cạnh tranh Ricoh",
            "time": "10:30",
            "scripts": [
                {"path": "scripts/seo_competitor_bounce.json", "delay": 10},
                {"path": "scripts/seo_ricoh_deep.json", "delay": 0}
            ]
        },
        {
            "name": "03. Báo giá & Cho thuê",
            "time": "14:00",
            "scripts": [
                {"path": "scripts/seo_price_check.json", "delay": 5},
                {"path": "scripts/seo_rental_service.json", "delay": 0}
            ]
        },
        {
            "name": "04. Chuyên gia tư vấn",
            "time": "16:30",
            "scripts": [
                {"path": "scripts/seo_comparison_study.json", "delay": 15},
                {"path": "scripts/seo_office_solutions.json", "delay": 0}
            ]
        },
        {
            "name": "05. Hỗ trợ kỹ thuật",
            "time": "20:30",
            "scripts": [
                {"path": "scripts/seo_technical_support.json", "delay": 5},
                {"path": "scripts/seo_brand_authority.json", "delay": 0}
            ]
        }
    ]

    start_date = datetime.now().strftime("%Y-%m-%d")

    for cp in campaigns:
        cursor.execute("""
            INSERT INTO schedules (name, profile_id, start_date, start_time, duration_days, is_active, scripts_json, run_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cp['name'],
            0, # Random profile
            start_date,
            cp['time'],
            30,
            1, # Active ON
            json.dumps(cp['scripts']),
            "Traffic Bot"
        ))

    conn.commit()
    conn.close()
    print("Successfully added 5 SEO campaigns to database!")

if __name__ == "__main__":
    setup_campaigns()
