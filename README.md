Sure! Here's a basic `README.md` file that explains the functionality of your Flask app:

---

# Flask Admin Dashboard with Google Login

This Flask application provides a simple admin dashboard with two types of login options:
1. **Admin Login**: Access to the dashboard is secured with a simple password (`admin123`).
2. **Google Login**: Users can log in via Google OAuth to access a user-specific dashboard.

### Features:
- **Admin Dashboard**: Displays user scores, visitor counts, and recent actions (log file).
- **Google Login Integration**: Users can log in using their Google account via OAuth2.
- **Simple Admin Password**: Admins can access the dashboard using a hardcoded password (`admin123`).

---

## Requirements

- Python 3.7+ (or compatible)
- Flask
- Flask-Dance (for Google OAuth integration)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/flask-admin-dashboard.git
   cd flask-admin-dashboard
   ```

2. Set up a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Google OAuth credentials:
   - Visit the [Google Developer Console](https://console.developers.google.com/).
   - Create a new project and enable the "Google+ API" and "OAuth 2.0" credentials.
   - Set up the OAuth consent screen and create OAuth 2.0 credentials.
   - Replace `"YOUR_GOOGLE_CLIENT_ID"` and `"YOUR_GOOGLE_CLIENT_SECRET"` in `app.py` with your actual credentials.

---

## Running the App

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. Visit the following routes in your browser:
   - **Home Page**: `/` - The welcome page.
   - **Admin Login**: `/admin` - Login with the password `admin123` to access the admin dashboard.
   - **Google Login**: `/google` - Log in with your Google account to view Google-specific user information.

---

## App Structure

- `app.py`: The main application logic for Flask, handling routes for the admin login, dashboard, and Google OAuth login.
- `templates/`:
  - `index.html`: The homepage of the app.
  - `admin_login.html`: The admin login page that asks for the password `admin123`.
  - `admin_dashboard.html`: The dashboard shown after admin login, displaying user data, visitor count, and recent actions.
  - `google_dashboard.html`: The page shown after Google login, displaying basic user info from Google.
- `log.txt`: A log file to track actions, used for displaying visitor count and recent activities.

---

## Customization

- **Password**: The default admin password is `admin123`. You can change this to any value by modifying the `admin_password` variable in `app.py`.
- **User Data**: The sample user data is currently hardcoded. You can replace this with a database or another source of data.
- **Google Login**: Make sure to set up your Google OAuth credentials as explained in the setup section.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to update the sections based on your project’s specific needs. Let me know if you need more details or adjustments!
