from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Reemplaza 'TU_API_KEY' con tu clave de API de Google Places
API_KEY = os.getenv('GOOGLE_API_KEY')

def find_place_id(place_name, location=None):
    url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    params = {
        'input': place_name,
        'inputtype': 'textquery',
        'fields': 'place_id',
        'key': API_KEY
    }
    if location:
        params['locationbias'] = f'point:{location}'
    response = requests.get(url, params=params)
    result = response.json()
    if result['candidates']:
        return result['candidates'][0]['place_id']
    return None

def get_place_details(place_id):
    url = f'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_phone_number',
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

@app.route('/get_place_info', methods=['GET'])
def get_place_info():
    place_name = request.args.get('place_name')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    if not place_name:
        return jsonify({'error': 'Se requiere el parámetro place_name'}), 400

    location = f'{lat},{lng}' if lat and lng else None
    place_id = find_place_id(place_name, location)
    if not place_id:
        return jsonify({'error': 'Lugar no encontrado'}), 404

    details = get_place_details(place_id)
    if 'result' in details:
        place_info = {
            'name': details['result'].get('name'),
            'phone_number': details['result'].get('formatted_phone_number')
        }
        return jsonify(place_info)
    else:
        return jsonify({'error': 'No se pudieron obtener los detalles del lugar'}), 500

if __name__ == '__main__':
    app.run(debug=True)
