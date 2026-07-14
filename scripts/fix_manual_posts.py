import json
import sqlite3
import shutil
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
vault_dir = _root / "outputs" / "runs"
legacy_dir = vault_dir / "published_archive" / "legacy_manual_posts"
ready_dir = vault_dir / "ready_to_upload"
db_path = _root / "outputs" / "db" / "content_state.db"
db_path.parent.mkdir(parents=True, exist_ok=True)

posts_data = {
    "Post_001_Types_Of_APIs": {
        "topic": "Types of APIs (REST, GraphQL, SOAP, WebSockets)",
        "caption": "Every software engineer needs to know this... 👇\n\nAPIs are the glue of the modern internet. But not all APIs are created equal. Are you still using REST for everything? \n\nHere is a quick breakdown:\n👉 REST: Good for standard CRUD ops.\n👉 GraphQL: Perfect for fetching exactly what you need (no over-fetching!).\n👉 SOAP: The old reliable for high-security enterprise apps.\n👉 WebSockets: Essential for real-time chat and trading apps.\n\nStop defaulting to REST when GraphQL or WebSockets might be better for your architecture.\n\nWhich API style do you use the most in your current project? Let me know below! 👇\n",
        "hashtags": ["#api", "#restapi", "#graphql", "#softwareengineering", "#coding", "#webdevelopment", "#backenddeveloper"]
    },
    "Post_002_SQL_Commands": {
        "topic": "Essential SQL Commands for Developers",
        "caption": "SQL is still the king of data. 👑👇\n\nYou can learn all the fancy new NoSQL databases, but relational databases (and SQL) aren't going anywhere anytime soon.\n\nIf you want to be a solid backend developer or data engineer, you MUST master these core SQL commands. From basic SELECTs to complex JOINs and aggregations, your data manipulation skills will set you apart from junior devs.\n\nSwipe through the carousel to see the SQL commands you'll use 90% of the time in production.\n\nSave this post for your next database interview! 💾\n\nWhat's your favorite database engine? PostgreSQL, MySQL, or something else?",
        "hashtags": ["#sql", "#database", "#dataengineering", "#postgres", "#mysql", "#codingtips", "#backenddevelopment", "#developer"]
    }
}

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

for folder_name, data in posts_data.items():
    src = legacy_dir / folder_name
    dst = ready_dir / folder_name
    
    if src.exists():
        # Move the folder
        shutil.move(str(src), str(dst))
        print(f"Moved {folder_name} to ready_to_upload.")
        
        # Reorganize PNGs
        png_folder = dst / "png"
        png_folder.mkdir(exist_ok=True)
        
        for file in dst.iterdir():
            if file.suffix.lower() == ".png":
                shutil.move(str(file), str(png_folder / file.name))
        
        # Write JSON
        pkg = {
            "topic": data["topic"],
            "narrative_arc": "Manual Creation",
            "caption": data["caption"],
            "hashtags": data["hashtags"]
        }
        (dst / "publish_package.json").write_text(json.dumps(pkg, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # Log to Database
        cursor.execute('''
            INSERT OR REPLACE INTO posts (run_id, topic, narrative_arc, status, caption, hashtags)
            VALUES (?, ?, ?, 'APPROVED', ?, ?)
        ''', (
            folder_name,
            data["topic"],
            "Manual Creation",
            data["caption"],
            json.dumps(data["hashtags"])
        ))
        
conn.commit()
conn.close()
print("✅ Manual posts upgraded and moved successfully.")
