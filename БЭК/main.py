from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

# Настройки базы данных
DB_URL = "sqlite:///users.db"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()

# Определение модели пользователя
class User(Base):
    __tablename__ = "negga"  # Измените на нужное имя таблицы
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    days = Column(Integer, default=False)

Base.metadata.create_all(engine)

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
    # Установка заголовков для поддержки CORS
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*") 
        self.send_header("Access-Control-Allow-Methods", "GET, POST")
        self.end_headers()

        # Извлечение username из URL
        path_parts = self.path.split('/')
        if True:
            username = path_parts[-1]
            user_data = self.get_user_data(username)
            if user_data:
                self.wfile.write(bytes(json.dumps(user_data), "utf-8"))
            else:
                self.wfile.write(bytes(json.dumps({"error": "User  not found"}), "utf-8"))
        else:
            self.wfile.write(bytes(json.dumps({"error": "Invalid request"}), "utf-8"))

    def get_user_data(self, username):
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        session.close()
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "days": user.days
            }
        return None

if __name__ == "__main__": 
    webServer = HTTPServer(("0.0.0.0", serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")