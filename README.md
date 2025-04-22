# Social Credit System

This project is a web-based karma points tracking system designed to monitor and manage user scores through positive and negative actions. It offers both a command-line interface and a web interface for ease of use.

## Features

- **User Management**: Add, view, and remove users
- **Points System**: Award positive points or deduct points from users
- **History Tracking**: Maintain a history of score changes
- **Ranking System**: View users ranked by their scores
- **Comments**: Users can leave comments
- **Admin Dashboard**: Access advanced management features
- **Visitor Analytics**: Track unique site visitors
- **Statistics**: View system statistics including averages, medians, and user activity

## Getting Started

### Prerequisites

- Python 3.6+
- Flask web framework

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/karma-points-system.git
cd karma-points-system
```

2. Install required packages
```bash
pip install flask
```

3. Run the application
```bash
python main.py
```

### Usage

#### Command Line Interface

When you run the application, you'll see a menu with these options:

1. Add Positive Action
2. Add Negative Action
3. View Score
4. View Rankings
5. Add New User
6. Remove User
7. View Unique Visitors
8. View System Statistics
9. Access Admin Dashboard (Web)
10. Exit

#### Web Interface

The web interface is available at:
- Main page: http://localhost:5000/
- Admin dashboard: http://localhost:5000/admin

### Admin Access

Admin access is restricted to authorized users in the `APPROVED_ADMINS` list in the code.

## Data Storage

The system stores data in three files:
- `users_data.json`: Contains all user data, scores, and history
- `visitor_log.txt`: Logs visitor information
- `ip_cache.json`: Caches visitor IP addresses to prevent duplicate logging

## Badge System

The system awards weekly badges to top performers every Sunday.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation
- Python statistics library
