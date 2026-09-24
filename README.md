# Library Management System

A console-based Library Management System built with Python using Object-Oriented Programming (OOP).

## Features

- Add new books
- Display all books
- Search books by title
- Search books by author
- Issue books to members
- Return books
- Remove books
- Prevent duplicate book IDs
- Validate user input
- Track borrowed books and members
- Save and load library data using JSON

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- JSON
- File Handling
- Exception Handling
- Dictionaries

## OOP Concepts Used

- Classes and Objects
- Encapsulation
- Methods
- Object interaction
- Separation of responsibilities between classes

## Data Persistence

The application stores book and borrower information in `library_data.json`.

When the application starts, existing data is loaded from the JSON file. Changes made during the session are saved so that the data remains available after restarting the application.

## How to Run

1. Clone the repository.
2. Open the project in PyCharm or another Python IDE.
3. Run `library_system.py`.
4. Follow the menu options displayed in the console.