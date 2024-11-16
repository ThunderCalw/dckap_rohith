# About
This is a Task given to me by DCKAP for interview process.
The Goal is to develop a prototype of a mockup Dashboard.

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
- PostgreSQL
- Slack API (for notifications)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ThunderCalw/dckap_rohith.git
cd `your-folder-name`
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
DB_USER="your-username"           `default = postgres`
DB_PASSWORD = "your-password"     `default = 1234`
DB_HOST="your-hostrname"           `default = localhost`
DB_PORT="your-port"                default = 5432`
DB_NAME="your-DB-name"
DB_URL = "postgresql+psycopg2://<DB_USER>:<DB_PASSWORD>@<DB_HOSTNAME>:<DB_PORT>/<DB_NAME>"
SLACK_OUTH = "your_slack_token_here"

```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

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

## Files(Explanation)

1. app.py  -  (`main file containing flask`)
2. create_db.py (`Used to initialize database`)
3. models.py (`used to hold the database structure template`)
4. web.py (`used for slack integration`)
5. index.html (`contains all html and javascript code`)

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
