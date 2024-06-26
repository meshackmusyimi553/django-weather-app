from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = '90db7e11fc05867489839078d70ee677'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    location = request.args.get('location')

    if not location:
        return jsonify({'error': 'Location is required'}), 400

    geocode_url = f'https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}'
    try:
        geocode_response = requests.get(geocode_url)
        if geocode_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch location data'}), 500

        geocode_data = geocode_response.json()
        if not geocode_data:
            return jsonify({'error': 'Location not found'}), 404

        lat = geocode_data[0]['lat']
        lon = geocode_data[0]['lon']

        weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'

        weather_response = requests.get(weather_url)
        forecast_response = requests.get(forecast_url)

        if weather_response.status_code != 200 or forecast_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch weather data'}), 500

        weather_data = weather_response.json()
        forecast_data = forecast_response.json()

        daily_forecasts = [item for item in forecast_data['list'] if '12:00:00' in item['dt_txt']][:5]

        return jsonify({
            'weather': weather_data,
            'forecast': daily_forecasts
        })

    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
