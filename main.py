import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from sap2012 import calculate_worksheet

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/calculate', methods=['POST'])
@cross_origin()
def calculate():
    data = request.get_json()
    result = {}
    # Just pulling out the SAP score and ECF for now, can contain CO2 emissions data etc
    for key, value in data.items():
        result[key] = {
            "name": key,
            "EER": calculate_worksheet(value)["SAP_rating"],
            "EIR": {
                "EI_rating": calculate_worksheet(value)["CO2_emissions"]["EI_rating"],
                "yearly_CO2": calculate_worksheet(value)["CO2_emissions"]["total_CO2_emissions_yearly"],
            }
        }
    response = result
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
