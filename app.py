from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def data_aqi(measurements):
    aqi_guide = {
        'pm25': "PM2.5 (İnce Partiküllü Madde)",
        'pm10': "PM10 (Kaba Partiküllü Madde)",
        'no2': "NO2 (Azot Dioksit)",
        'o3': "O3 (Ozon)",
        'so2': "SO2 (Kükürt Dioksit)",
        'co': "CO (Karbon Monoksit)"
    }

    interpreted_data = []
    for measurement in measurements:
        parameter = measurement['parameter']
        value = measurement['value']
        unit = measurement['unit']
        parameter_name = aqi_guide.get(parameter, parameter)

      
        if parameter == 'pm25' and value > 12:
            health_message = "Sağlık açısından zararlı seviyelerde."
        elif parameter == 'pm10' and value > 50:
            health_message = "Sağlık açısından zararlı seviyelerde."
        elif parameter == 'no2' and value > 100:
            health_message = "Sağlık açısından zararlı seviyelerde."
        elif parameter == 'o3' and value > 90:
            health_message = "Sağlık açısından zararlı seviyelerde."
        elif parameter == 'so2' and value > 400:
            health_message = "Sağlık açısından zararlı seviyelerde."
        elif parameter == 'co' and value > 10:
            health_message = "Sağlık açısından zararlı seviyelerde."
        else:
            health_message = "Normal seviyelerde."
        
        interpreted_data.append(f"- {parameter_name}: {value} {unit}. {health_message}")
    
    return interpreted_data


def get_air_quality_by_city(city, api_key):
    url = "https://api.openaq.org/v1/latest"
    params = {'city': city, 'limit': 5}  
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            measurements = data['results'][0]['measurements']
            return measurements
        else:
            return None
    else:
        return f"Error: {response.status_code}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        measurements = get_air_quality_by_city(city, api_key)
        if measurements:
            interpreted_data = data_aqi(measurements)
            return render_template('index.html', measurements=interpreted_data, city=city)
        else:
            error = "Bu şehir için veri bulunamadı."
            return render_template('index.html', error=error)
    return render_template('index.html')

api_key = "3a37cbec5e1b42cf50cf4f0b51a7d3c8e1c39ad65751eebfda00dfbaa189ba62"

if __name__ == '__main__':
    app.run(debug=True)
