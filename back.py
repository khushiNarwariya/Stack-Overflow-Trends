from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load and process the dataset
file_path = "stackoverflow_data_ordered.csv"
df = pd.read_csv(file_path)

# Convert Upload Time column to datetime
df['year'] = pd.to_datetime(df['year'])
df['Year'] = df['year'].dt.year  # Extract the year
df['Tag'] = df['Tag'].str.split(';')  # Convert tags column into a list

# Explode dataset to get individual tags per row
df_exploded = df.explode('Tag')

# Count occurrences of each tag per year
tag_counts = df_exploded.groupby(['Year', 'Tag']).size().unstack(fill_value=0)

# Normalize by total tags per year
tag_totals_per_year = tag_counts.sum(axis=1)
relative_trend = tag_counts.div(tag_totals_per_year, axis=0) * 100  # Convert to percentage

def get_chart_data():
    data = {
        "labels": relative_trend.index.astype(str).tolist(),
        "datasets": []
    }
    
    # Get the top 10 tags by total occurrences
    top_tags = tag_counts.sum().nlargest(10).index
    
    # Define colors for each tag
    colors = [
        'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)',
        'rgba(199, 199, 199, 1)', 'rgba(83, 102, 255, 1)', 'rgba(40, 159, 64, 1)',
        'rgba(230, 102, 255, 1)'
    ]
    
    # Add each tag's data
    for i, tag in enumerate(top_tags):
        data["datasets"].append({
            "label": tag,
            "data": relative_trend[tag].fillna(0).tolist(),
            "borderColor": colors[i % len(colors)],
            "backgroundColor": colors[i % len(colors)].replace('1)', '0.2)'),
            "fill": False
        })
    
    return data

@app.route('/')
def index():
    return render_template('idx.html')

@app.route('/api/data')
def api_data():
    return jsonify(get_chart_data())

if __name__ == '__main__':
    app.run(debug=True)
