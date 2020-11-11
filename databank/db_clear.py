from app import app, db
meta = db.metadata
for table in reversed(meta.sorted_tables):
    db.session.execute(table.delete())
db.session.commit()
