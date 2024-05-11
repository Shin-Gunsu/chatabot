from flask import Flask, request, jsonify, abort, render_template
import socket
import json
from flask_cors import CORS
# 챗봇 엔진 서버 정보
host = "127.0.0.1"      # 챗봇 엔진 서버 IP
port = 5050             # 챗봇 엔진 port

# Flask 애플리케이션
app = Flask(__name__)
CORS(app)
# 챗봇 엔진 서버와 통신
def get_answer_from_engine(query):
    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청
    json_data = {
        'query' : query
    }
    
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()

    return ret_data

# 챗봇 엔진 query 전송 API
@app.route('/query', methods=['POST'])
def query():
    body = request.get_json()
    try:
        # 일반 질의응답 API
        ret = get_answer_from_engine(query=body['query'])
        return jsonify(ret)

    except Exception as ex:
        # 오류 발생 시 500 Error
        abort(500)

@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    try:
        # bot서버로 id, pw전달
        
        mySocket = socket.socket()
        mySocket.connect((host, port))
        message = json.dumps(body)
        mySocket.send(message.encode())

        data = mySocket.recv(2048).decode()
        print(data)
        ret_data = json.loads(data)
        print(ret_data)
        mySocket.close()
        

        return jsonify(ret_data)

    except Exception as ex:
        # 오류 발생 시 500 Error
        abort(500)


@app.route('/')
def hello():
    return '하이룽'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)