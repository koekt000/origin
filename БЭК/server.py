from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import func


DB_URL = "sqlite:///tasks.db"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()
class Task(Base):
        __tablename__ = "task"
        id = Column(Integer, primary_key=True, autoincrement=True)
        number =  Column(Integer)
        task = Column(String)
        answer = Column(String)
        explain = Column(String)
Base.metadata.create_all(engine)

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
        

        path_parts = self.path.split('/')
        try:
            id = path_parts[-1]
            if path_parts[-2] == "daily":
                user_data = self.get_random_task()
            else:
                user_data = self.get_task(int(path_parts[-2]))
                
            if user_data:
                self.wfile.write(bytes(json.dumps(user_data), "utf-8"))
            else:
                self.wfile.write(bytes(json.dumps({"error": "User  not found"}), "utf-8"))
        except:
            self.wfile.write(bytes(json.dumps({"error": "Invalid request"}), "utf-8"))

    def get_random_task(self):
        session = Session()
        user = session.query(Task).filter_by().order_by(func.random()).first()
        session.close()
        if user:
            return {
                "question": user.task,
                "answer": user.answer[1:],
                "explanation": user.explain
            }
        return None
    def get_task(self, number):
        session = Session()
        user = session.query(Task).filter_by(number=number).order_by(func.random()).first()
        print(user)
        session.close()
        if user:
            return {
                "question": user.task,
                "answer": user.answer[1:],
                "explanation": user.explain
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