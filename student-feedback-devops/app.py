from flask import Flask, request, redirect, url_for, jsonify
from datetime import datetime
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

# Ensure persistent data directory
DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)
DB_URL = f"sqlite:///{os.path.join(DATA_DIR, 'feedback.db')}"

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

@app.get("/")
def index():
    # Simple inline HTML to avoid templates folder
    with SessionLocal() as db:
        last = db.query(Feedback).order_by(Feedback.created_at.desc()).limit(5).all()
    items = "".join(
        f"<li><strong>{f.name}</strong> ({f.email}) — {f.message} "
        f"<small>{f.created_at.strftime('%Y-%m-%d %H:%M')}</small></li>"
        for f in last
    )
    html = f'''
    <html>
      <head>
        <title>Student Feedback</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
          body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; padding: 24px; max-width: 720px; margin: auto; }}
          .card {{ padding:16px; border:1px solid #ddd; border-radius:12px; margin-bottom:16px; }}
          input, textarea {{ width:100%; padding:10px; border:1px solid #ccc; border-radius:8px; margin:6px 0 12px; }}
          button {{ padding: 10px 14px; border:0; border-radius:8px; background:#111827; color:white; }}
        </style>
      </head>
      <body>
        <h1>Student Feedback Web App</h1>
        <div class="card">
          <form method="POST" action="/feedback">
            <label>Name</label>
            <input name="name" required />
            <label>Email</label>
            <input name="email" type="email" required />
            <label>Message</label>
            <textarea name="message" rows="3" required></textarea>
            <button type="submit">Submit</button>
          </form>
        </div>
        <div class="card">
          <h3>Latest feedback (5)</h3>
          <ul>{items or "<li>No feedback yet. Be the first!</li>"}</ul>
        </div>
        <div class="card">
          <p>Health: <code>/health</code></p>
        </div>
      </body>
    </html>
    '''
    return html

@app.post("/feedback")
def submit():
    name = request.form.get("name","").strip()
    email = request.form.get("email","").strip()
    message = request.form.get("message","").strip()
    if not (name and email and message):
        return "All fields are required", 400
    with SessionLocal() as db:
        f = Feedback(name=name, email=email, message=message)
        db.add(f)
        db.commit()
    return redirect(url_for("index"))

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
