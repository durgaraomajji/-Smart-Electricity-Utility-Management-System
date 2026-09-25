from app.models.notification import Notification


def create_notification(db, user_id, title, message):
    n=Notification(user_id=user_id,title=title,message=message)
    db.add(n); db.flush(); return n
