from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import random

# Initialize Flask application
app = Flask(__name__)

# Load the trained models
autoencoder_model = load_model('encoder_model.h5')
classifier_model = load_model('classifier.h5')

min_val = [1000, 1000, 1000, 1000, 1000, 1000, 1000]
max_val = [-1000, -1000, -1000, -1000, -1000, -1000, -1000]
crop_info = {
  'jowar': {
    'benefits': 'Jowar is rich in fiber, protein, and essential nutrients. It is gluten-free and helps in weight management and digestive health.',
    'time_to_grow': 'early_variety : 80-90 days , late_variety : 100-120 days, seasons_per_year : Varies depending on region, typically one or two',
    'estimated_cost_per_kg': 'Rs 8-12 (Source: [ICAR - Jowar Cultivation Practices](https://www.icar.org.in/icar-research/crops/sorghum.htm))',
    'profit_margin': 'Average 50%, can vary depending on market conditions (Source: [Government of India - Market Analysis Report on Pulses](https://www.krishiudyog.com/pulse-market-analysis-report/))'
  },
  'rice': {
    'benefits': 'Rice is a staple food for a large part of the world\'s human population, providing more than one-fifth of the calories consumed worldwide.',
    'time_to_grow': 'Varies depending on variety (60-150 days). Short-grain varieties mature faster than long-grain. (Source: [FAO - Rice Production](http://www.fao.org/agriculture/crops/rice/production/en/))',
    'estimated_cost_per_kg': 'Rs 7-10 (Source: [Government of India - Market Analysis Report on Rice](https://www.krishiudyog.com/rice-market-analysis-report/))',
    'profit_margin': 'Average 40%, can vary depending on market conditions (Source: [同上](https://www.krishiudyog.com/rice-market-analysis-report/))'  # Same source as previous rice entry
  },
  'wheat': {
    'benefits': 'Wheat is a staple food crop that provides a significant amount of carbohydrates and dietary fiber. It is versatile and can be used to make various food products.',
    'time_to_grow': 'Varies depending on variety (140-160 days for winter wheat). Spring wheat matures faster (around 110-130 days). (Source: [USDA - Wheat Production](https://www.ers.usda.gov/topics/crops/wheat/background/))',
    'estimated_cost_per_kg': 'Rs 10-14 (Source: [Government of India - Market Analysis Report on Wheat](https://www.krishiudyog.com/wheat-market-analysis-report/))',
    'profit_margin': 'Average 45%, can vary depending on market conditions (Source: [同上](https://www.krishiudyog.com/wheat-market-analysis-report/))'  # Same source as previous wheat entry
  },
  'arhar': {
    'benefits': 'Arhar, also known as pigeon pea, is a pulse crop that is rich in protein, fiber, and other essential nutrients. It is commonly used in Indian cuisine.',
    'time_to_grow': 'Typically 150-180 days, but can vary depending on variety. (Source: [ICAR - Pigeonpea Cultivation Practices](https://www.icar.org.in/icar-research/crops/pigeonpea.htm))',
    'estimated_cost_per_kg': 'Rs 14-18 (Source: [Government of India - Market Analysis Report on Pulses](https://www.krishiudyog.com/pulse-market-analysis-report/))',
    'profit_margin': 'Average 55%, can vary depending on market conditions (Source: [同上](https://www.krishiudyog.com/wheat-market-analysis-report/))'  # Same source as previous pulses entry
  },  'bajra': {
    'benefits': 'Bajra, or pearl millet, is a drought-resistant crop that is rich in protein, fiber, and micronutrients. It is commonly used in Indian cuisine.',
    'time_to_grow': 'Typically 60-90 days. (Source: [ICAR - Bajra Cultivation Practices](https://www.icar.org.in/icar-research/crops/bajra.htm))',
    'estimated_cost_per_kg': 'Rs 9-13 (Source: [Government of India - Market Analysis Report on Millets](https://www.krishiudyog.com/millets-market-analysis-report/))',
    'profit_margin': 'Average 40%, can vary depending on market conditions (Source: [同上](https://www.krishiudyog.com/millets-market-analysis-report/))'  # Same source as millets entry
  },
  'millet': {
    'benefits': 'Millet is a nutritious gluten-free grain rich in protein, fiber, and iron. It is known for its digestibility and is a good source of antioxidants.',
    'time_to_grow': 'Varies depending on variety, typically 70-85 days. (Source: [USDA National Agricultural Library - Foxtail Millet](https://www.nal.usda.gov/nalcat/catalog/9780160931701))',
    'estimated_cost_per_kg': 'Rs 30-40 (Source: [Organic Facts - Foxtail Millet](https://www.organicfacts.net/health-benefits/foxtail-millet.html))',  # Broader price range due to specialty grain
    'profit_margin': 'Data on specific profit margin for foxtail millet is limited.'
  },
  'barley': {
    'benefits': 'Barley is a whole grain cereal rich in fiber, vitamins, and minerals. It can be used in various food products like bread, soups, and stews.',
    'time_to_grow': 'Varies depending on variety (80-110 days for spring barley, 140-160 days for winter barley). (Source: [Iowa State University - Barley Production](https://store.extension.iastate.edu/product/C6-43))',
    'estimated_cost_per_kg': 'Rs 12-16 (Source: [Agrocrops Market News - Barley](https://www.agrocrops.com/barley-price-india.html))',
    'profit_margin': 'Average 45%, can vary depending on market conditions (Source: [Source to be confirmed - ongoing research])'  # Research needed for specific barley profit margin
  },
  'gram': {
    'benefits': 'Gram, also known as urad dal, is a pulse crop rich in protein, fiber, and essential nutrients. It is commonly used in Indian cuisine for dals and lentil dishes.',
    'time_to_grow': 'Typically 100-130 days. (Source: [ICAR - Urad Cultivation Practices](https://www.icar.org.in/icar-research/crops/pulses/blackgram.htm))',
    'estimated_cost_per_kg': 'Rs 40-50 (Source: [Government of India - Market Analysis Report on Pulses](https://www.krishiudyog.com/pulse-market-analysis-report/))',
    'profit_margin': 'Average 50%, can vary depending on market conditions (Source: [同上](https://www.krishiudyog.com/pulse-market-analysis-report/))'  # Same source as previous pulses entry
  },'maize': {
  'benefits': 'Maize, also known as corn, is a versatile cereal crop rich in carbohydrates and essential nutrients. It is used for food, animal feed, and industrial products.',
  'time_to_grow': 'Varies depending on variety and climate (typically 110-150 days). (Source: [USDA - Corn and Sorghum Production](https://www.ers.usda.gov/topics/crops/corn-and-sorghum/background/))',
  'estimated_cost_per_kg': 'Rs 7-9 (Source: [**Department of Agriculture, Cooperation and Farmers Welfare, Government of India**](https://www.dacfw.gov.in/))',  # Placeholder, replace with actual source when found
  'profit_margin': 'Average data not readily available. Profitability can vary depending on factors like production costs, market prices, and government subsidies.'
},
  'ragi': {
  'benefits': 'Ragi, also known as finger millet, is a gluten-free grain rich in protein, fiber, calcium, and iron. It is known for its drought resistance and nutritional value.',
  'time_to_grow': 'Typically 90-120 days. (Source: [ICAR - Ragi Cultivation Practices](https://www.icar.org.in/icar-research/crops/cereals/ragi.htm))',
  'estimated_cost_per_kg': 'Rs 25-35 (Source: [Krishi Jagran - Ragi Price in India](https://www.krishijagran.com/agriculture-news/ragi-price-in-india-today-per-kg-mandi-bhav-2023-24-14733))',
  'profit_margin': 'Average 40%, can vary depending on market conditions (Source: [Agri Business Today - Ragi Farming Profit](https://www.agribusinesstoday.in/ragi-farming-profit-margin-and-cost-of-cultivation/))'
} }


# Run the Flask app
def adjust_dataframe_length(df, target_length):
    # Check if df.shape[0] is less than the target length
    if df.shape[0] < target_length:
        df = pd.concat([df, df.tail(target_length - df.shape[0])])

    # Check if df.shape[0] is greater than the target length
    if df.shape[0] > target_length:
        # Create a list of rows where the 4th column (precip) value is 0
        zero_precip_rows = []
        for i in range(len(df)):
            # if df.iloc[i, 3] == 0:
            zero_precip_rows.append(i)

        # Randomly select rows from the list of zero_precip_rows
        rows_to_remove = random.sample(zero_precip_rows, df.shape[0] - target_length)

        # Remove the selected rows from the DataFrame
        df = df.drop(rows_to_remove)
    return df

# Normalize the data using Min-Max scaling
def min_max_scaling(df, min_val, max_val):
    for i, col in enumerate(df.columns):
        df[col] = (df[col] - min_val[i]) / (max_val[i] - min_val[i])
    return df

def append_rows_to_single_row(df):
    # Normalize each column separately
    # Normalize the data using Min-Max scaling
    df_normalized = min_max_scaling(df, min_val, max_val)

    # Create an empty dictionary to store the data
    data_dict = {}

    # Number of days
    num_days = len(df_normalized)

    # Iterate over each row
    for i in range(num_days):
        # Get the data from the current row
        row_data = df_normalized.iloc[i].values

        # Append the data to the dictionary with modified column names
        for j, value in enumerate(row_data):
            column_name = f"{df_normalized.columns[j]}_day_{i+1}"
            data_dict[column_name] = value

    # Convert the dictionary to a DataFrame
    single_row_df = pd.DataFrame([data_dict])

    return single_row_df

def calculate_min_max(df):
    global min_val, max_val
    for i, col in enumerate(df.columns):
        min_val[i] = min(df[col].min(), min_val[i])
        max_val[i] = max(df[col].max(), max_val[i])


def load_and_adjust_data(json_data_list, target_length):
    # Convert JSON data to DataFrame
    df = pd.DataFrame(json_data_list)
    print("Type after pd.DataFrame:", type(df))

    # Specify the columns to read from the DataFrame
    columns_to_read = ["temp", "dew", "humidity", "cloudcover", "solarradiation", "solarenergy", "uvindex"]
    
    # Read only the specified columns from the DataFrame
    df = df[columns_to_read]
    
    # Fill NaN values with column means
    df = df.fillna(df.mean())
    
    if df.isna().any().any():
        print("NaN values encountered in DataFrame.")
    
    # Calculate min and max values for scaling
    calculate_min_max(df)
    
    # Adjust the length of the DataFrame
    df = adjust_dataframe_length(df, target_length)
    
    return df



def extract_label_from_url(url):
    filename = url.split('/')[-1]  # Get the filename from the URL
    label = re.split('_\d+', filename)[1]  # Extract the label based on the pattern
    return label[1:]

def filter_crops(crop_list, key):
    filtered_list = []
    for crop_info in crop_list:
        if key in crop_info:
            filtered_list.append(crop_list[key])
    return filtered_list

def predict_categories_from_data(urls, encoder_model, classifier_model):
    # Load and adjust the data
    datas = load_and_adjust_data(urls, 180)

    # Convert each DataFrame to a single row
    single_row_datas = append_rows_to_single_row(datas)
    print("hello xxxxxxxxxxxxxxxxxxxxxxxx", type(single_row_datas.shape), single_row_datas)

    # Concatenate the single-row DataFrames
    # datas_concatenated = pd.concat(single_row_datas, axis=0)

    # Use the trained encoder model to extract features from the reconstructed data
    encoded_reconstructed_data = encoder_model.predict(single_row_datas.values.reshape(single_row_datas.shape[0], single_row_datas.shape[1], 1))
    print("bello xxxxxxxxxxxxxxxxxxxxxxxx", len(encoded_reconstructed_data[0]), encoded_reconstructed_data[0])

    # Make predictions on the reconstructed data using the classifier model
    predictions = classifier_model.predict(encoded_reconstructed_data)

    # Convert predicted probabilities into class labels
    predicted_labels = np.argmax(predictions, axis=1)

    # Map the class labels to their corresponding categories
    category_mapping = {0: 'jowar', 1: 'rice', 2: 'wheat',3:'arhar',4: 'bajra',5: 'barley',6: 'gram',7: 'maize',8: 'ragi',9:'urad'}
    predicted_categories = [category_mapping[label] for label in predicted_labels]

    return predicted_categories

# Define routes
@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.json
    category = predict_categories_from_data(data,autoencoder_model,classifier_model)
    filtered_crops = filter_crops(crop_info, category[0])

    return jsonify({'predicted_category': category[0].capitalize(),'details': filtered_crops })

if __name__ == '__main__':
    app.run(debug=True)
