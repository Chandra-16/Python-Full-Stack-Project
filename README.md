## EnergyFlo - Home Energy Usage Breakdown

EnergyFlo is a smart and easy-to-use tool that helps you see and manage how your home uses electricity. It does more than just look at your final bill—it breaks down your energy use for each appliance, showing you what's happening in real-time.

With EnergyFlo, you can find out which of your devices use the most power and watch your usage patterns over time. The app has a friendly dashboard with simple charts and graphs that make all this information easy to understand. This helps you find wasteful habits, make smarter choices, and lower both your electricity bills and your impact on the environment. EnergyFlo gives you the facts you need to run a more efficient and eco-friendly home.

## ✨ Key Features

- **📊 Dynamic Dashboard** : Get a clear, visual breakdown of your energy consumption with interactive charts and graphs powered by Streamlit.

- **⚡️ Real-Time Tracking**: Easily log energy usage data for different appliances, rooms, or the entire home.

- **🏠 Appliance-Level Insights**: Pinpoint your biggest "energy hogs" and see how each device contributes to your total consumption.

- **📈 Trend Analysis**: Visualize your energy usage over time (daily, weekly, and monthly) to identify patterns and track your progress.

- **💸 Cost Estimator**: See the financial impact of your energy habits with an estimated cost breakdown based on consumption.

- **🔗 Modern Backend**: A robust API built with FastAPI ensures high performance and reliable data handling.

- **🔒 Secure & Scalable Database**: Your data is safely stored in a flexible and powerful Supabase database.

## Project Structure
```
EnergyFlo/                                        # Main project directory
├── .env                                          # 🔐 Environment variables for sensitive data (e.g., Supabase keys)
├── README.md                                     # 📝 Project overview, features, and setup instructions
├── requirements.txt                              # 📦 List of all Python dependencies for the project
│
├── API/                                          # ⚙️ Directory for the FastAPI backend
│   └── main.py                                   # 🚀 The main entry point for the API endpoints
│
├── frontend/                                     # 💻 Directory for the Streamlit frontend
│   └── app.py                                    # 📊 The main Streamlit application script
│
└── src/                                          # 📁 Directory for reusable source code and business logic
    ├── __init__.py                               # 📜 Makes 'src' a Python package
    ├── db.py                                     # 💾 Module for all Supabase database interactions
    └── logic.py                                  # 🧠 Module for business logic and data processing
```
## 🚀 Getting Started

# Prerequisites
- Python 3.8+ installed
- A Supabase account and a project URL/API key
- pip package manager

### 1. Clone the Repository

    git clone https://github.com/Chandra-16/Python-Full-Stack-Project.git
    cd EnergyFlo

### 2. Set up your environment:

    python -m venv venv
    source venv/bin/activate

### 3. Install the dependencies:

    pip install -r requirements.txt

### 4. Configuration
- Create a .env file in the root directory and add your Supabase credentials.

    SUPABASE_URL=YOUR_SUPABASE_URL
    SUPABASE_KEY=YOUR_SUPABASE_API_KEY

### 5. How to Run

1. Start the FastAPI backend:
    uvicorn main:app --reload

2. In a new terminal, run the Streamlit app:
    streamlit run app.py

## 🛠️ Technologies Used

- **Frontend**:
    - Streamlit: For building the interactive, Python-native dashboard.

- **Backend**:
    - FastAPI: A high-performance Python web framework for building the API.
    - Uvicorn: An ASGI server to run the FastAPI application.

- **Database**:
    - Supabase: The open-source Firebase alternative, providing a PostgreSQL database, API, and authentication.

## 📂 Project Structure & Key Components
This project is built with a clear separation of concerns, dividing the application into a high-performance backend API and a user-friendly frontend dashboard.

- **`src/db.py`**: This is your database module. It handles all the code for connecting to Supabase and managing data (reading, writing, and updating records).

- **`src/logic.py`**: This is where the core logic lives. It contains the "smart" functions that process and analyze the raw data from db.py to create meaningful insights and visualizations.

- **`API/main.py`**: This is your backend API, built with FastAPI. It's the central hub that receives requests from the frontend and uses the functions from the src folder to get the right data.

- **`frontend/app.py`**: This is your Streamlit app. It's the user interface where all the buttons, charts, and tables are displayed. It gets its data by making requests to the FastAPI backend.


## 🌟 Future Enhancements

- **User Authentication & Profiles**: Implement user sign-up and login using Supabase Auth to allow multiple users to securely track their own data. This will include creating individual user profiles to manage preferences and home settings.

- **Automated Data Input**: Move beyond manual data entry. We plan to integrate with smart plugs, IoT devices, and utility provider APIs (like Home Assistant) to automatically collect energy consumption data.

- **Predictive Analytics**: Use machine learning models to analyze historical data and predict future energy consumption. This could provide users with a forecast of their next bill and help them budget more effectively.

- **Personalized Savings Suggestions**: Based on a user's unique energy profile, the app will offer actionable tips to reduce consumption. For example, suggesting a user run their dryer during off-peak hours to save money.

- **Cost & Carbon Tracking**: Expand the cost analysis to include a carbon footprint calculator. Users will be able to see the environmental impact of their energy usage and track their progress toward sustainability goals.

- **Alerts & Notifications**: Implement a system to send alerts for unusual activity, such as a spike in consumption that might indicate a faulty appliance.

- **Reporting**: Introduce an automated reporting feature that can generate and email a summary of monthly energy usage and savings.
