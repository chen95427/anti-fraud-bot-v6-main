"""Render 預設用 gunicorn app:app，這個檔案讓它能正確找到 Flask app。"""
from server import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
