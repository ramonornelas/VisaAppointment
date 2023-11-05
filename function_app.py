import azure.functions as func
import json
from modules import check_dates
from modules import get_cookie_from_file

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def get_parameter(req, param_name, expected_type, default_value):
  param_value = req.params.get(param_name, default=default_value)
  try:
    return expected_type(param_value)
  except ValueError:
    return (f"Invalid value for {param_name}")

@app.route(route="endpoint")
def endpoint(req:func.HttpRequest) -> func.HttpResponse:

    # city_id = int(req.params.get('cityId'))
    city_id = get_parameter(req, 'cityId', int, None)
    user = get_parameter(req, 'user', str, None)
    # computer_name = get_parameter(req, 'computerName', str, None)
    # mocked_data_count = get_parameter(req, 'mockedDataCount', int, None)
    # start_date = get_parameter(req, 'startDate', str, None)

    cookie = get_cookie_from_file()
    target_date = '2024-10-29'

    city_names = {
        65: "Ciudad Juarez",
        66: "Guadalajara",
        67: "Hermosillo",
        68: "Matamoros",
        69: "Merida",
        70: "Mexico City",
        71: "Monterrey",
        72: "Nogales",
        73: "Nuevo Laredo",
        74: "Tijuana",
    }

    city_name = city_names.get(city_id, "Invalid case")
    check_dates_result = check_dates(city_id, city_name, target_date, cookie, user)
    response = {
        f"result": f"{city_name + ': ' + check_dates_result}"
    }
    
    headers = {
        "Access-Control-Allow-Origin": "*",  # Specify the allowed origin or use "*" for all
        "Access-Control-Allow-Methods": "GET, POST",  # Specify allowed HTTP methods
        "Access-Control-Allow-Headers": "Content-Type",  # Specify allowed headers
    }
    
    return func.HttpResponse(
        body=json.dumps(response),
        mimetype="application/json",
        status_code=200,
        headers=headers
    )