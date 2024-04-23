from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
  data = {
    "nombre": "raspberry",
    "id": 44,
    "ubicacion": "Florida Universitaria",
  }
  return jsonify(data)

@app.route('/raspberry')
def raspberry():
  data = {
    "id": 44,
    "valores": obtener_valores()
  }
  return jsonify(data)

def obtener_valores():

        voltaje =  round(random.uniform(11, 12),3)
        corriente = round(random.uniform(0, 1),3)
        potencia = round(voltaje*corriente,3)
        temperatura = round(random.uniform(24, 25),2)
        
        res = {
          "voltaje":voltaje,
          "corriente": corriente,
          "potencia":potencia,
          "temperatura":temperatura
        }

        return res

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=50100, debug=True)