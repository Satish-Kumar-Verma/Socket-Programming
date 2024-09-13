
# Socket Programming in Python - Version 1.0 and 2.0

Welcome to **Socket Programming** in Python. This repository demonstrates client-server communication using TCP protocol, with both **single-connection** (Version 1.0) and **multi-threaded concurrent connections** (Version 2.0) implementations. The project supports both normal users for surveys and admin users for server monitoring.

## 🚀 Features

### Version 1.0 (Single Connection)
- **Admin Panel**: Root user authentication to view survey data.
- **Survey System**: Clients can submit surveys.
- **Single Connection**: Only one client can connect to the server at a time.
- **Real-Time Data Transfer**: Logs and displays survey data in real-time for the admin.

### Version 2.0 (Multiple Concurrent Connections)
- **Admin Panel**: Allows root users to log in and view the survey data.
- **Multi-Threading**: Supports multiple concurrent client connections.
- **Survey System**: Similar survey mechanism as Version 1.0 with enhanced functionality.
- **Security**: Admin credentials are handled more securely.

---

## 📁 Project Structure

```
Socket-Programming/
│
├── TCP/
│   ├── Version 1.0/
│   │   ├── admin.py        # Single connection admin panel
│   │   ├── client.py       # Client program for survey
│   │   ├── server.py       # Server for handling single connection
│   │   ├── helper.py       # Helper functions for credentials and data handling
│   │   └── survey_data.csv  # Stored survey data
│
│   ├── Version 2.0/
│   │   ├── admin.py        # Multi-threaded admin panel
│   │   ├── client.py       # Client program for survey
│   │   ├── server.py       # Server for handling multiple concurrent connections
│   │   ├── helper.py       # Helper functions for credentials and session handling
│   │   └── survey_data.csv  # Stored survey data
```

---

## 📦 Installation

### Prerequisites
- Python 3.x
- [PrettyTable](https://pypi.org/project/prettytable/)

### Clone the repository
```bash
git clone https://github.com/Satish-Kumar-Verma/Socket-Programming.git
cd Socket-Programming - TCP/
```

### Install required dependencies
```bash
pip install -r requirements.txt  # Install PrettyTable if not already installed
```

---

## 🛠 How to Run

### Version 1.0 (Single Connection)

1. Start the server:
   ```bash
   python Version\ 1.0/server.py
   ```

2. Run the client to perform a survey:
   ```bash
   python Version\ 1.0/client.py
   ```

3. Admin can view the results by running the admin panel:
   ```bash
   python Version\ 1.0/admin.py
   ```

### Version 2.0 (Multiple Concurrent Connections)

1. Start the server:
   ```bash
   python Version\ 2.0/server.py
   ```

2. Run multiple clients to perform surveys:
   ```bash
   python Version\ 2.0/client.py
   ```

3. Admin can log in and view the results using the admin panel:
   ```bash
   python Version\ 2.0/admin.py
   ```

---

## 📓 TCP Socket Programming Concepts

### Client-Server Model
Both versions use a client-server architecture. In Version 1.0, only one client can connect to the server at a time, whereas Version 2.0 supports multiple clients simultaneously using threads. Admin authentication allows the server admin to view and manage survey data.

---

## 🧑‍💻 Contributing

We welcome contributions! Feel free to submit issues, bug reports, or feature requests. If you'd like to contribute code, please:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add a new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Support

For questions or support, open an issue or contact me at [email@example.com](mailto:email@example.com).

---

Happy coding! 😊
