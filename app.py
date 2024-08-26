from flask import Flask, render_template, request
import requests

app = Flask(__name__)

ALPHA_VANTAGE_API_KEY = '6HGZZW5INLMPNOA3'  # Replace with your actual API key

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    current_price = None
    predicted_price = None
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        prediction, current_price, predicted_price = predict(stock_symbol)
    return render_template('index.html', prediction=prediction, current_price=current_price, predicted_price=predicted_price)

# def fetch_real_time_price(stock_symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=1min&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        latest_timestamp = max(data['Time Series (1min)'].keys())  # Get the latest timestamp
        latest_price = float(data['Time Series (1min)'][latest_timestamp]['4. close'])
        return latest_price
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None
    except (KeyError, ValueError) as e:
            print("Error parsing data:", e)
            return None
def fetch_real_time_price(stock_symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=1min&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if "Note" in data:
            print("API limit reached. Please try again later.")
            return None
        if 'Time Series (1min)' not in data:
            print(f"Invalid response for symbol {stock_symbol}: {data}")
            return None
        latest_timestamp = max(data['Time Series (1min)'].keys())  # Get the latest timestamp
        latest_price = float(data['Time Series (1min)'][latest_timestamp]['4. close'])
        return latest_price
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None
    except (KeyError, ValueError) as e:
        print("Error parsing data:", e)
        return None

def predict(stock_symbol):
    current_price = fetch_real_time_price(stock_symbol)

    if current_price is None:
        return 'Error fetching data', None, None

    predicted_percentage_increase = 0.02  # 2% predicted increase (modify as needed)
    predicted_price = current_price * (1 + predicted_percentage_increase)

    prediction = 'Buy' if predicted_price > current_price else 'Sell'

    return prediction, current_price, predicted_price

if __name__ == "__main__":
    app.run(host="0.0.0.0")


