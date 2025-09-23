# 🎵 Chinook Music Store - Desktop Application

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/github/license/mehranmohammadiii/MusicStore)
![GitHub stars](https://img.shields.io/github/stars/mehranmohammadiii/MusicStore?style=social)
![GitHub forks](https://img.shields.io/github/forks/mehranmohammadiii/MusicStore?style=social)

A fully-functional desktop application for managing the Chinook Music Store, built with **Python**, **Tkinter**, and **SQL Server**. This project demonstrates a robust **3-Layer Architecture** and advanced software engineering principles.

---

## 🚀 Live Demo (GIF)

*A brief demonstration of the application's core functionalities, including navigation, data retrieval, and the responsive UI.*

![App Demo GIF]()


---

## ✅ Core Features

-   **View Bestselling Tracks:** Get a real-time, scrollable list of the top-selling music tracks from the database.
-   **Browse Artist Albums:** View a comprehensive list of all albums, neatly grouped by artist.
-   **Explore Invoices:** Look up personal invoice history with a simple and intuitive interface.
-   **Create New Invoices:** A complete, multi-step form to create new customer invoices and add items to the order.
-   **Responsive UI:** The application window can be resized, and all components will gracefully adjust their layout, demonstrating a modern approach to desktop UI design.

-   ## 🏛️ Architectural & Technical Highlights

The primary goal of this project was to implement professional software architecture and design patterns to create a maintainable, scalable, and robust application.

### 1. **3-Layer Architecture**
The application is strictly divided into three logical layers to ensure separation of concerns, maintainability, and scalability:
-   **UI (User Interface Layer):** Built with Tkinter. Responsible only for displaying data and capturing user input. It has no knowledge of the database.
-   **BLL (Business Logic / Service Layer):** The "brain" of the application. It handles validation, business rules, and orchestrates calls between the UI and DAL.
-   **DAL (Data Access Layer):** The only layer that communicates with the database. It is responsible for executing SQL queries and Stored Procedures.
-   
![Architecture Diagram](https://github.com/mehranmohammadiii/MusicStore/blob/master/APP/MyPackage/UI/Images/_%D9%86%D9%85%D9%88%D8%AF%D8%A7%D8%B1%20%D8%A8%D8%AF%D9%88%D9%86%20%D9%86%D8%A7%D9%85_.drawio%20(1).png)
### 2. **Dependency Injection (DI) Pattern**
Instead of using a global Singleton, the database connection manager is created once at application startup and **injected** into the service layer, which then injects it into the data access layer. This makes the code:
-   **Transparent:** Dependencies are explicit and clear.
-   **Highly Testable:** Allows for mocking the database connection during unit tests.
-   **Flexible:** Easily adaptable for different database configurations.

### 3. **Advanced SQL Server Integration**
-   **Stored Procedures:** All business logic is executed through stored procedures, keeping the application code clean from complex SQL queries.
-   **Triggers:** Advanced triggers are used to enforce complex business rules (like preventing duplicate daily invoices) directly within the database.
-   **Graceful Error Handling:** The application gracefully handles `RAISERROR` messages from SQL triggers and displays user-friendly error messages, demonstrating a robust integration between the application and database layers.

### 4. **External Configuration**
The database connection string is not hard-coded. It is read from an external `config.ini` file, allowing any user to easily configure the application for their own database server.

### 5. **Executable Creation**
The entire application is packaged into a single, standalone **`.exe` file** using `PyInstaller`, making it easy to distribute and run on any Windows machine.

---

## 📦 Project Structure

The project follows a standardized and scalable structure, making it easy to navigate and maintain.

```plaintext

Chinook-Desktop-App/
│
├── MyPackage/
│   ├── __init__.py         # Marks 'MyPackage' as a Python package
│   ├── UI/                 # UI Layer: Tkinter forms, windows, and custom widgets
│   ├── services/           # Business Logic Layer: Service classes coordinating operations
│   └── database/           # Data Access Layer: DAL classes and DB connection logic
│
├── Images/                # Contains assets like images and diagrams for this README
│
├── main.py                 # The main entry point to run the application
├── requirements.txt        # A list of all required Python packages for the project
├── config.ini              # External database configuration file for easy setup
└── README.md               # You are here!

```
---

## 🛠️ Getting Started: Installation & Usage

This guide provides instructions for both end-users who just want to run the application and developers who want to work with the code.

### 🅰️ For End-Users (The Easy Way)

This method is for anyone who wants to run the application without dealing with the source code.

**1. Download the Application:**
- Go to the **[Releases](https://github.com/mehranmohammadiii/MusicStore)** page of this repository.
- Find the latest version (e.g., `v1.0.0`) and download the `MusicStore_v1.0.zip` .

**2. Prerequisites:**
- **Database:** You need access to a SQL Server instance with the **Chinook** database restored on it.
- **Driver:** Install the official Microsoft ODBC Driver for SQL Server. This is a small, one-time installation.
  - **[Download Link for ODBC Driver 17](https://aka.ms/msodbcsql17)**

**3. Configuration and Execution:**
- **Unzip** the downloaded `MusicStore_v1.0.zip` file. You will find three items inside: `main.exe`, `config.ini`, and `README.txt`.
- Open the `config.ini` file with a text editor (like Notepad).
- Enter your own SQL Server connection details (Server name, Database name, etc.).
- Save and close the `config.ini` file.
- Double-click `main.exe` to run the application and enjoy!

### 🅱️ For Developers (The Advanced Way)

This method is for developers who want to run the source code, inspect it, or contribute to the project.

**1. Clone the Repository:**
```bash
git clone https://github.com/mehranmohammadiii/MusicStore.git
cd MusicStore

**2. Create and Activate a Virtual Environment:**
A virtual environment is highly recommended to keep dependencies isolated.
# Create the environment
python -m venv venv

# Activate it
# On Windows (PowerShell/CMD):
.\venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

**3. Install Required Packages:**
All dependencies are listed in the requirements.txt file.
pip install -r requirements.txt

**4. Configure the Database:**
Ensure the Chinook database is running on your SQL Server instance and is accessible.
Edit the config.ini file with your server details, just like the end-users.

**5. Run the Application:**
python main.py


