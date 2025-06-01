# Medicine Expiry Tracker

A comprehensive web application for tracking medicine expiry dates, managing inventory, and receiving notifications before medicines expire.

## Features

- **Medicine Management**: Add, edit, view, and delete medicines with details like name, batch number, expiry date, quantity, etc.
- **Expiry Tracking**: Automatically calculates days until expiry and categorizes medicines as expired, expiring soon, near expiry, or safe.
- **Dashboard**: Visual overview of medicine inventory with filtering options.
- **QR Code Generation**: Generate QR codes for each medicine for easy access to details.
- **User Management**: Multiple user roles (admin, staff, regular user) with appropriate permissions.
- **Notifications**: Email notifications for medicines nearing expiry.
- **Data Export**: Export medicine data to CSV format.
- **Responsive Design**: Works on desktop and mobile devices.
- **Dark Mode**: Toggle between light and dark themes.

## Technology Stack

- **Backend**: Django (Python web framework)
- **Database**: MongoDB (via Djongo)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Django's built-in authentication system
- **Styling**: Bootstrap 5, Font Awesome icons
- **PDF Generation**: ReportLab
- **QR Code Generation**: qrcode

## Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB
- Git

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/medicine-tracker.git
   cd medicine-tracker
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # MongoDB settings
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_NAME=medicine_tracker
   
   # Email settings
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## Usage

### Admin User

1. Log in with the superuser credentials.
2. Access the admin panel at http://127.0.0.1:8000/admin/ to manage users, medicines, and categories.
3. Create new users and assign roles (admin, staff, regular user).

### Regular User

1. Register a new account or log in with provided credentials.
2. Add medicines with details like name, category, batch number, expiry date, etc.
3. View the dashboard to see an overview of all medicines.
4. Filter medicines by name, category, or expiry status.
5. Update profile settings, including email notification preferences.

## Project Structure

```
medicine_tracker/
├── medicines/              # Medicine management app
│   ├── admin.py           # Admin configurations
│   ├── forms.py           # Forms for medicine data
│   ├── models.py          # Medicine and Category models
│   ├── urls.py            # URL patterns for medicine views
│   └── views.py           # Views for medicine operations
├── users/                  # User management app
│   ├── admin.py           # Admin configurations
│   ├── forms.py           # Forms for user data
│   ├── models.py          # User profile model
│   ├── urls.py            # URL patterns for user views
│   └── views.py           # Views for user operations
├── medicine_tracker/       # Project settings
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL patterns
│   └── wsgi.py            # WSGI configuration
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User-uploaded files
├── .env                    # Environment variables
├── manage.py               # Django management script
└── requirements.txt        # Project dependencies
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [MongoDB](https://www.mongodb.com/)