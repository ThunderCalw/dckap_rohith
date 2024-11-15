# About
This is a Task given to me by DCKAP for interview process.
The Goal is to develop a Dashboard mockup as show in the given file.

# Test Case Management System

A Flask-based web application for managing test cases in a hierarchical module structure. The system allows users to organize test cases within modules, supports file attachments, and includes Slack notifications for test case changes.

## Features

- 📊 Hierarchical module management with parent-child relationships
- ✅ Create, read, update, and delete test cases
- 📁 File attachment support for test cases
- 🌲 Tree view visualization of modules
- 🔔 Slack integration for test case notifications
- 📱 Responsive web interface

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy ORM , PostgreSQL
- **Frontend**: HTML, CSS, JavaScript (with tree view implementation)
- **UI Components**: Bootstrap for modals and layout
- **Notifications**: Slack API integration

## Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- python-dotenv
- Slack API credentials (for notifications)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd test-case-management
```

2. Create a virtual environment and activate it:
```bash
Create   : python -m venv venv
Activate : venv\Scripts\activate.bat
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```
DB_URL=sqlite:///test_cases.db
SLACK_TOKEN=your_slack_token_here
SLACK_CHANNEL=your_channel_here
```

## Running the Application

1. Initialize the database:
```bash
python create_db.py
```

2. Start the Flask server:
```bash
python app.py
```

3. Access the application at `http://localhost:5000`

## Usage

### Modules
- Create new modules with optional parent modules
- View module hierarchy in tree structure
- Delete modules (cascades to child modules and test cases)

### Test Cases
- Add test cases to any module
- Edit test case details (title and description)
- Attach files to test cases
- Download attached files
- Delete test cases

### Notifications
The system automatically sends Slack notifications for:
- New test case creation
- Test case updates
- Test case deletion

## API Endpoints

### Modules
- `GET /` - Home page with module tree
- `GET /module/<module_id>` - Get module details and test cases
- `POST /module` - Create new module
- `DELETE /module/<module_id>` - Delete module

### Test Cases
- `POST /testcase` - Create new test case
- `GET /testcase/<testcase_id>` - Get test case details
- `PUT /testcase/<testcase_id>` - Update test case
- `DELETE /testcase/<testcase_id>` - Delete test case

### File Management
- `POST /testcase/<testcase_id>/upload` - Upload file attachment
- `GET /download/<testcase_id>` - Download file attachment

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
