from email_sender import app as celery_app

if __name__ == "__main__":
    celery_app.start()
