# EquiHealth - Health Disparity Analysis Platform

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Railway](https://img.shields.io/badge/deploy-railway-purple.svg)](https://railway.app)

EquiHealth is a comprehensive web platform for analyzing and visualizing health disparities across different geographical regions. This alternate version uses matplotlib for data visualization and machine learning for predictive health analytics.

## 🌟 Features

- **Interactive Health Data Analysis**: Upload CSV files with health indicators for analysis
- **Machine Learning Predictions**: AI-powered health outcome predictions using XGBoost
- **Geographical Visualization**: Generate interactive maps showing health disparities by district
- **User Authentication**: Secure login/signup system with session management
- **Data Export**: Download prediction results as CSV files
- **Responsive Design**: Mobile-friendly interface for accessibility

## 🔧 Technology Stack

- **Backend**: Flask (Python)
- **Machine Learning**: Scikit-learn, XGBoost, Joblib
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, GeoPandas
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Railway, Gunicorn

## 📊 Supported Health Indicators

- TB Incidence Rate
- Diabetes Prevalence
- Malaria Incidence Rate
- HIV/AIDS Prevalence
- Infant Mortality Rate (IMR)
- Vaccination Coverage
- Socioeconomic Factors (Income, Employment, Education)
- Environmental Factors (Air Quality Index, Rainfall)
- Infrastructure (Housing, Urbanization)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/MaheshR03/equihealth-alternate.git
   cd equihealth-alternate
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the platform**
   Open your browser and navigate to `http://localhost:5000`

### 🌐 Deploy to Railway

This application is ready for one-click deployment to Railway:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

## 📁 Project Structure

```
equihealth-alternate/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment config
├── runtime.txt           # Python version specification
├── health-data/          # ML models and scalers
│   ├── predictionmodel.pkl
│   └── scaler.pkl
├── static/               # Static assets
│   ├── styles.css
│   ├── scripts.js
│   ├── health_data.csv
│   └── maps/            # Generated map visualizations
├── templates/           # HTML templates
│   ├── frontpage.html
│   ├── upload.html
│   ├── result.html
│   └── ...
└── README.md
```

## 🎯 Usage

1. **Sign Up/Login**: Create an account or log in to access the platform
2. **Upload Data**: Upload a CSV file with health indicators for your districts
3. **View Predictions**: Get AI-powered health outcome predictions
4. **Visualize Results**: Generate geographical maps showing health disparities
5. **Export Data**: Download prediction results for further analysis

### Sample Data Format

Your CSV should include columns for:
- District, Latitude, Longitude
- Health indicators (TB Incidence, Diabetes Prevalence, etc.)
- Socioeconomic factors (Income Level, Employment Rate, etc.)
- Environmental data (AQI, Annual Rainfall, etc.)

## 🖼️ Platform Preview

![EquiHealth Platform](image.png)

*Interactive health disparity visualization showing district-wise health rankings and predictions*

## 🔒 Security Features

- Secure password hashing with Werkzeug
- Session-based authentication
- Environment variable configuration for production
- CSRF protection ready
- Input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original [Equihealth](https://github.com/MaheshR03/equihealth) project
- Flask and Python communities
- Open source health data initiatives
- Railway for deployment platform

## 📞 Support

For questions, issues, or contributions:
- Create an [Issue](https://github.com/MaheshR03/equihealth-alternate/issues)
- Submit a [Pull Request](https://github.com/MaheshR03/equihealth-alternate/pulls)
- Contact: [maheshr3002@gmail.com]

---

**Built with ❤️ for better health outcomes and data-driven decision making**
