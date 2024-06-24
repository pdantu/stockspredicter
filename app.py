# from flask import Flask, render_template, request
# import pandas as pd
# import os

# app = Flask(__name__)

# # Directories
# CSV_FOLDER = 'metrics'
# RESULTS_FOLDER = 'results'
# PORTFOLIO_FOLDER = 'portfolio'

# app.config['CSV_FOLDER'] = CSV_FOLDER
# app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
# app.config['PORTFOLIO_FOLDER'] = PORTFOLIO_FOLDER

# # List of available sectors (11 SPDR ETF sectors)
# SECTORS = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLB', 'XLRE', 'XLK', 'XLU']

# @app.route('/')
# def home():
#     return render_template('indexx.html')

# @app.route('/metrics', methods=['GET', 'POST'])
# def metrics():
#     selected_sector = None
#     data = None
#     if request.method == 'POST':
#         selected_sector = request.form['sector']
#         file_path = os.path.join(app.config['CSV_FOLDER'], f'{selected_sector}-metrics.csv')
#         if os.path.exists(file_path):
#             data = pd.read_csv(file_path)
#         else:
#             data = None

#     return render_template('metrics.html', sectors=SECTORS, selected_sector=selected_sector, data=data)

# @app.route('/action', methods=['GET', 'POST'])
# def action():
#     selected_sector = None
#     data = None
#     if request.method == 'POST':
#         selected_sector = request.form['sector']
#         file_path = os.path.join(app.config['RESULTS_FOLDER'], f'{selected_sector}-action.csv')
#         if os.path.exists(file_path):
#             data = pd.read_csv(file_path)
#         else:
#             data = None

#     return render_template('action.html', sectors=SECTORS, selected_sector=selected_sector, data=data)

# @app.route('/portfolios', methods=['GET', 'POST'])
# def portfolios():
#     portfolio_type = None
#     data = None
#     if request.method == 'POST':
#         portfolio_type = request.form['portfolio']
#         file_path = os.path.join(app.config['PORTFOLIO_FOLDER'], f'portfolio{portfolio_type.lower()}.csv')
#         if os.path.exists(file_path):
#             data = pd.read_csv(file_path)
#         else:
#             data = None

#     return render_template('portfolios.html', portfolio_type=portfolio_type, data=data)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Directories
RESULTS_FOLDER = 'results'
MERGED_CSV_PATH = 'merged.csv'
CSV_FOLDER = 'metrics'
PORTFOLIO_FOLDER = 'portfolio'
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['CSV_FOLDER'] = CSV_FOLDER
app.config['PORTFOLIO_FOLDER'] = PORTFOLIO_FOLDER
# List of available sectors (11 SPDR ETF sectors)
SECTORS = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLB', 'XLRE', 'XLK', 'XLU']

def merge_csv_files():
    all_data = pd.DataFrame()
    for sector in SECTORS:
        file_path = os.path.join(app.config['RESULTS_FOLDER'], f'{sector}-action.csv')
        if os.path.exists(file_path):
            sector_data = pd.read_csv(file_path)
            # Add a 'Sector' column to identify which sector each row belongs to
            sector_data['Sector'] = sector
            all_data = pd.concat([all_data, sector_data], ignore_index=True)
    all_data.to_csv(MERGED_CSV_PATH, index=False)

# Merge CSV files on application startup
merge_csv_files()

# Load merged CSV into DataFrame
merged_data = pd.read_csv(MERGED_CSV_PATH)

@app.route('/')
def home():
    return render_template('indexx.html')

@app.route('/metrics', methods=['GET', 'POST'])
def metrics():
    selected_sector = None
    data = None
    if request.method == 'POST':
        selected_sector = request.form['sector']
        file_path = os.path.join(app.config['CSV_FOLDER'], f'{selected_sector}-metrics.csv')
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
        else:
            data = None

    return render_template('metrics.html', sectors=SECTORS, selected_sector=selected_sector, data=data)

@app.route('/action', methods=['GET', 'POST'])
def action():
    selected_sector = None
    data = None
    if request.method == 'POST':
        selected_sector = request.form['sector']
        file_path = os.path.join(app.config['RESULTS_FOLDER'], f'{selected_sector}-action.csv')
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
        else:
            data = None

    return render_template('action.html', sectors=SECTORS, selected_sector=selected_sector, data=data)

@app.route('/portfolios', methods=['GET', 'POST'])
def portfolios():
    portfolio_type = None
    data = None
    if request.method == 'POST':
        portfolio_type = request.form['portfolio']
        file_path = os.path.join(app.config['PORTFOLIO_FOLDER'], f'portfolio{portfolio_type.lower()}.csv')
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
        else:
            data = None

    return render_template('portfolios.html', portfolio_type=portfolio_type, data=data)

@app.route('/search_stock', methods=['GET', 'POST'])
def search_stock():
    df = pd.read_csv('merged.csv')
    search_result = None
    if request.method == 'POST':
        stock_tickers = request.form['stock_ticker'].upper().split(',')
        stock_tickers = [ticker.strip() for ticker in stock_tickers]
        search_result = df[df['Ticker'].isin(stock_tickers)]
        if search_result.empty:
            search_result = None

    return render_template('search_stock.html', search_result=search_result)
# def search_stock():
#     # Merge CSV files before searching
#     # merge_csv_files()
#     df = pd.read_csv('merged.csv')
#     search_result = None
#     if request.method == 'POST':
#         stock_ticker = request.form['stock_ticker'].upper()
#         search_result = df[df['Ticker'] == stock_ticker]
#         print(search_result)
#         if search_result.empty:
#             search_result = None
#         print(search_result)
#     return render_template('search_stock.html', search_result=search_result)

if __name__ == '__main__':
    app.run(debug=True)
