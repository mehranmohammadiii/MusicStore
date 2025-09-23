# 🎵 Chinook Music Store - Desktop Application

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/github/license/mehranmohammadiii/MusicStore)
![GitHub stars](https://img.shields.io/github/stars/mehranmohammadiii/MusicStore?style=social)
![GitHub forks](https://img.shields.io/github/forks/mehranmohammadiii/MusicStore?style=social)

A fully-functional desktop application for managing the Chinook Music Store, built with **Python**, **Tkinter**, and **SQL Server**. This project demonstrates a robust **3-Layer Architecture** and advanced software engineering principles.

---

## 🚀 Live Demo (GIF)

*A brief demonstration of the application's core functionalities, including navigation, data retrieval, and the responsive UI.*

![App Demo GIF](https://raw.githubusercontent.com/mehranmohammadiii/MusicStore/main/_assets/demo.gif)
_**(Please replace this with your own GIF's raw URL after uploading!)**_

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

![Architecture Diagram](https://raw.githubusercontent.com/mehranmohammadiii/MusicStore/main/_assets/architecture-diagram.png)
_**(Please replace this with your own diagram's raw URL after uploading!)**_

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

---
