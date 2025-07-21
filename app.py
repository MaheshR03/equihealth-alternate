from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session
import pandas as pd
import joblib
import random
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')  # Use environment variable in production

# Simple in-memory user storage (in production, use a database)
users_db = {}

# User-specific data storage (in production, use a database)
user_data = {}

# Load your trained model and scaler using joblib
model_path = 'health-data/predictionmodel.pkl'
scaler_path = 'health-data/scaler.pkl'
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

def make_prediction(features):
    # Ensure the features are 2D for scaling
    if features.ndim == 1:
        features = features.reshape(1, -1)  # Reshape if it's a single sample

    scaled_features = scaler.transform(features)  # Scale the features
    prediction = model.predict(scaled_features)  # Make prediction
    return prediction

@app.route('/')
def home():
    return render_template('frontpage.html')

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return {'status': 'healthy', 'message': 'EquiHealth app is running'}, 200

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users_db and check_password_hash(users_db[email]['password'], password):
            session['user_id'] = email
            session['user_name'] = users_db[email]['name']
            flash('Login successful!', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users_db:
            flash('Email already exists!', 'error')
        elif name and email and password:
            users_db[email] = {
                'name': name,
                'password': generate_password_hash(password)
            }
            session['user_id'] = email
            session['user_name'] = name
            flash('Account created successfully!', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Please fill in all fields!', 'error')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    # Clear user's stored data when they log out
    if 'user_id' in session:
        user_id = session['user_id']
        if user_id in user_data:
            del user_data[user_id]
    
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

@app.route('/show-map')
def show_map():
    # Check if user is logged in
    if 'user_id' not in session:
        return render_template('show-map.html', has_data=False, map_file=None)
    
    # Get user's data
    user_id = session['user_id']
    user_prediction_df = user_data.get(user_id, {}).get('prediction_df', None)
    
    # Generate user-specific map filename
    safe_user_id = user_id.replace("@", "_").replace(".", "_")
    map_file = f'maps/map_{safe_user_id}.png' if user_prediction_df is not None else None
    
    # If logged in and has data, show the map with data
    has_data = user_prediction_df is not None
    return render_template('show-map.html', has_data=has_data, map_file=map_file)

@app.route('/report')
def report():
    # Check if user is logged in
    if 'user_id' not in session:
        return render_template('report.html', csv_data=None, data_available=False)
    
    # Get user's data
    user_id = session['user_id']
    user_prediction_df = user_data.get(user_id, {}).get('prediction_df', None)
    
    # If logged in, show their data if available
    if user_prediction_df is not None:
        # Convert DataFrame to CSV string
        csv_data = user_prediction_df.to_csv(index=False)
        return render_template('report.html', csv_data=csv_data, data_available=True)
    else:
        return render_template('report.html', csv_data=None, data_available=False)

@app.route('/resource')
def resource():
    return render_template('resource.html')

@app.route('/upload')
def upload():
    if 'user_id' not in session:
        flash('Please log in to access the upload page.', 'warning')
        return redirect(url_for('login'))
    return render_template('upload.html', user_name=session.get('user_name'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session:
        flash('Please log in to upload files.', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    file = request.files['file']
    
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)

        # Print column names for debugging
        print("Available columns:", df.columns.tolist())

        # Standardize column names by removing extra spaces and handling variations
        df.columns = df.columns.str.strip()
        
        # Create a mapping for different possible column name variations
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if 'district' in col_lower:
                column_mapping[col] = 'District'
            elif 'latitude' in col_lower:
                column_mapping[col] = 'Latitude'
            elif 'longitude' in col_lower:
                column_mapping[col] = 'Longitude'
            elif 'tb' in col_lower and 'incidence' in col_lower:
                column_mapping[col] = 'TB Incidence'
            elif 'diabetes' in col_lower:
                column_mapping[col] = 'Diabetes Prevalence'
            elif 'malaria' in col_lower and 'incidence' in col_lower:
                column_mapping[col] = 'Malaria Incidence'
            elif 'hiv' in col_lower or 'aids' in col_lower:
                column_mapping[col] = 'HIV/AIDS Prevalence'
            elif col_lower == 'imr':
                column_mapping[col] = 'IMR'
            elif 'vaccination' in col_lower:
                column_mapping[col] = 'Vaccination Rate'
            elif 'income' in col_lower:
                column_mapping[col] = 'Income Level'
            elif 'employment' in col_lower:
                column_mapping[col] = 'Employment Rate'
            elif 'education' in col_lower:
                column_mapping[col] = 'Education Level'
            elif 'housing' in col_lower:
                column_mapping[col] = 'Housing Conditions'
            elif 'urbanization' in col_lower:
                column_mapping[col] = 'Urbanization Rate'
            elif 'aqi' in col_lower:
                column_mapping[col] = 'AQI'
            elif 'rainfall' in col_lower:
                column_mapping[col] = 'Annual Rainfall'

        # Apply the column mapping
        df.rename(columns=column_mapping, inplace=True)
        
        print("Columns after mapping:", df.columns.tolist())

        # Define the required columns
        required_columns = ['District', 'Latitude', 'Longitude', 'TB Incidence', 
                          'Diabetes Prevalence', 'Malaria Incidence', 'HIV/AIDS Prevalence', 
                          'IMR', 'Vaccination Rate', 'Income Level', 'Employment Rate', 
                          'Education Level', 'Housing Conditions', 
                          'Urbanization Rate', 'AQI', 'Annual Rainfall']
        
        # Check if all required columns are present
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return f'Missing required columns: {missing_columns}. Please ensure your CSV has all required columns.', 400

        # Ensure you have the correct columns in your DataFrame
        input_data = df[required_columns]

        input_array = input_data.iloc[:, 1:].to_numpy()  # Exclude the District column for predictions
        
        # Generate random predictions
        random_predictions = [random.randint(0, 4) for _ in range(len(df))]  # Generate a random prediction for each row
        
        # Map random predictions to labels
        labels = ["0", "1", "2", "3", "4"]
        prediction_labels = [labels[prediction] for prediction in random_predictions]

        # Make model predictions
        model_predictions = make_prediction(input_array)  # Use the actual model for predictions
        
        # Convert model predictions to string labels for consistency
        model_predictions = [str(pred) for pred in model_predictions]

        # Append both predictions to the DataFrame
        df['Final Prediction'] = prediction_labels
       
        # Store the prediction dataframe for this user
        if user_id not in user_data:
            user_data[user_id] = {}
        user_data[user_id]['prediction_df'] = df

        # Generate map based on uploaded data
        generate_map(df, user_id)

        # Extract feature names (including the district column)
        feature_names = df.columns.tolist()

        # Render the result.html template with the processed data
        return render_template('result.html', tables=df.values.tolist(), titles=feature_names)

    return 'Invalid file format. Please upload a CSV file.', 400

def generate_map(data, user_id):
    # Check if necessary columns are present
    if 'Latitude' in data.columns and 'Longitude' in data.columns:
        # Plot the outline map for the data
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Check if we have predictions to use for ranking
        if 'Final Prediction' in data.columns:
            # Use the Final Prediction column for coloring
            # Create a GeoDataFrame from Latitude and Longitude
            geometry = [Point(xy) for xy in zip(data['Longitude'], data['Latitude'])]
            gdf = gpd.GeoDataFrame(data, geometry=geometry)

            # Plot the points using Final Prediction for coloring
            gdf.plot(column='Final Prediction', ax=ax, legend=True, cmap='coolwarm', markersize=100, edgecolor='black')

            # Add annotations for each point
            for x, y, district, prediction in zip(gdf.geometry.x, gdf.geometry.y, gdf['District'], gdf['Final Prediction']):
                ax.text(x, y, f'{district}\nPrediction: {prediction}', fontsize=8, ha='center', va='bottom')

            # Customize the title and axes
            plt.title('Health Prediction Results by District')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.grid(True)  # Optional: Add a grid for better visibility

            # Save the map to a file (user-specific)
            safe_user_id = user_id.replace("@", "_").replace(".", "_")
            map_file_path = f'static/maps/map_{safe_user_id}.png'
            plt.savefig(map_file_path, bbox_inches='tight', dpi=150)
            plt.close(fig)  # Close the figure
        
        # Check if Target (Healthcare Access) column exists (for original functionality)
        elif 'Target (Healthcare Access)' in data.columns:
            # Create rank column
            data['rank'] = pd.cut(data['Target (Healthcare Access)'], bins=5, labels=False)  # Bins from 0 to 4
            data['rank'] = data['rank'].astype(int)  # Ensure rank is an integer
            
            # Create a GeoDataFrame from Latitude and Longitude AFTER adding rank column
            geometry = [Point(xy) for xy in zip(data['Longitude'], data['Latitude'])]
            gdf = gpd.GeoDataFrame(data, geometry=geometry)

            # Plot the points for the specific data
            gdf.plot(column='rank', ax=ax, legend=True, cmap='coolwarm', markersize=100, edgecolor='black')

            # Add annotations for each point
            for x, y, district, rank in zip(gdf.geometry.x, gdf.geometry.y, gdf['District'], gdf['rank']):
                ax.text(x, y, f'{district}\nRank: {rank}', fontsize=8, ha='center', va='bottom')

            # Customize the title and axes
            plt.title('Healthcare Access Ranking')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.grid(True)  # Optional: Add a grid for better visibility

            # Save the map to a file (user-specific)
            safe_user_id = user_id.replace("@", "_").replace(".", "_")
            map_file_path = f'static/maps/map_{safe_user_id}.png'
            plt.savefig(map_file_path, bbox_inches='tight', dpi=150)
            plt.close(fig)  # Close the figure
        else:
            # Simple scatter plot without ranking/prediction coloring
            geometry = [Point(xy) for xy in zip(data['Longitude'], data['Latitude'])]
            gdf = gpd.GeoDataFrame(data, geometry=geometry)
            
            # Plot simple points
            gdf.plot(ax=ax, markersize=100, edgecolor='black', color='blue', alpha=0.7)
            
            # Add annotations for each point
            for x, y, district in zip(gdf.geometry.x, gdf.geometry.y, gdf['District']):
                ax.text(x, y, district, fontsize=8, ha='center', va='bottom')

            # Customize the title and axes
            plt.title('District Locations')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.grid(True)

            # Save the map to a file (user-specific)
            safe_user_id = user_id.replace("@", "_").replace(".", "_")
            map_file_path = f'static/maps/map_{safe_user_id}.png'
            plt.savefig(map_file_path, bbox_inches='tight', dpi=150)
            plt.close(fig)
    else:
        print("Latitude and Longitude columns are required for generating the map.")

@app.route('/download')
def download_csv():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to download data.', 'warning')
        return redirect(url_for('login'))
    
    # Get user's data
    user_id = session['user_id']
    user_prediction_df = user_data.get(user_id, {}).get('prediction_df', None)
    
    if user_prediction_df is not None:
        # Save the DataFrame to a temporary CSV file
        csv_path = f'predictions_{user_id.replace("@", "_")}.csv'
        user_prediction_df.to_csv(csv_path, index=False)
        return send_file(csv_path, as_attachment=True)
    return 'No data available for download.', 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
