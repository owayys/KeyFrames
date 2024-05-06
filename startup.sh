apt update
apt-get install -y libGL
gunicorn --bind=0.0.0.0 --workers=4 main:app --port 8000