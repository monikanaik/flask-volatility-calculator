from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import os

app = Flask(__name__)


@app.route('/calculate_volatility', methods=['POST'])
def calculate_volatility():
    """
    Calculate Daily and Annualized Volatility.

    Parameters:
    - file: Upload a CSV file.
    - directory_path: Directory path to fetch data from. If provided, file parameter is ignored.

    Returns:
    - JSON response containing the daily volatility and annualized volatility.
    """
    try:
        # Check if a file is provided or use data from the directory
        if 'file' in request.files:
            file = request.files['file']
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
        elif 'directory_path' in request.form:
            directory_path = request.form['directory_path']
            # Assuming the directory contains CSV files and we want to analyze the first file found
            file_list = pd.Series(os.listdir(directory_path))
            csv_file = file_list[file_list.str.endswith('.csv')].iloc[0]
            df = pd.read_csv(os.path.join(directory_path, csv_file))
        else:
            return jsonify({"error": "Either provide a file or a directory_path parameter."}), 400

        # Calculate daily returns
        df['daily_returns'] = df['Close'] / df['Close'].shift(1) - 1

        # Drop the first row which contains NaN in 'daily_returns'
        df = df.dropna(subset=['daily_returns'])

        # Calculate daily volatility
        daily_volatility = df['daily_returns'].std()

        # Calculate annualized volatility (assuming 252 trading days per year)
        annualized_volatility = daily_volatility * np.sqrt(252)

        # Return the results
        result = {"daily_volatility": daily_volatility, "annualized_volatility": annualized_volatility}
        return jsonify(result)

    except pd.errors.EmptyDataError:
        return jsonify({"error": "The provided CSV file is empty."}), 400

    except pd.errors.ParserError:
        return jsonify({"error": "Error parsing the CSV file. Make sure it is in the correct format."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
