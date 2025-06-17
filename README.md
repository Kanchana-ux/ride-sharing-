# RideShare Two-Wheeler - Python Flask Data Structures Project

A comprehensive two-wheeler ride-sharing web application built with **Python Flask backend** and **React frontend**, demonstrating practical usage of various Python data structures and algorithms for a Project-Based Learning (PBL) course.

## 🎯 Project Overview

RideShare connects drivers and riders for efficient, cost-effective two-wheeler transportation. This project showcases the implementation of core Python data structures and algorithms in a real-world application.

## 🚀 Features

### Core Functionality
- **User Authentication**: Registration and login system with role-based access (Driver/Rider)
- **Driver Features**:
  - Post ride offers with details (origin, destination, time, available seats, price)
  - Manage ride requests from riders
  - Accept/decline ride requests
  - View earnings and ride statistics
- **Rider Features**:
  - Search for available rides with advanced filters
  - Send ride requests to drivers
  - View request status and ride history
- **Real-time Updates**: Live status updates for rides and requests

## 🐍 Python Data Structures Implementation

This project demonstrates practical usage of various Python data structures:

### 1. **Lists**
- **Usage**: Storing collections of rides, users, and ride requests
- **Implementation**: 
  ```python
  active_rides = []  # List of active ride IDs
  search_history = []  # List of recent searches (FIFO queue)
  ```
- **Benefits**: Sequential access, easy iteration, dynamic sizing, O(1) append

### 2. **Dictionaries (Hash Maps)**
- **Usage**: Fast user lookups, caching, and data mapping
- **Implementation**:
  ```python
  user_sessions = {}  # {user_id: session_data}
  ride_cache = {}  # {ride_id: ride_data}
  driver_rides = {}  # {driver_id: [ride_ids]}
  ```
- **Benefits**: O(1) average lookup time, efficient key-value storage

### 3. **Sets**
- **Usage**: Ensuring uniqueness and efficient membership testing
- **Implementation**:
  ```python
  unique_emails = set()  # Set of registered emails
  active_drivers = set()  # Set of currently active driver IDs
  blocked_users = set()  # Set of blocked user IDs
  ```
- **Benefits**: O(1) membership testing, automatic uniqueness

### 4. **Classes and Objects**
- **Usage**: Structured data representation and encapsulation
- **Implementation**:
  ```python
  class User(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      first_name = db.Column(db.String(100), nullable=False)
      role = db.Column(db.String(10), nullable=False)  # 'driver' or 'rider'
      
  class Ride(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      driver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
      origin = db.Column(db.String(200), nullable=False)
      
  class RideRequest(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      ride_id = db.Column(db.Integer, db.ForeignKey('rides.id'))
      status = db.Column(db.String(20), default='pending')
  ```
- **Benefits**: Data encapsulation, inheritance, method binding

### 5. **Tuples**
- **Usage**: Immutable coordinate pairs and fixed-size data groupings
- **Implementation**:
  ```python
  popular_routes = [
      ("Mumbai Central", "Bandra"),
      ("Pune Station", "Hadapsar"),
      ("Delhi CP", "Gurgaon")
  ]
  ```
- **Benefits**: Immutable grouped data, semantic meaning

## 🛠 Tech Stack

### Backend (Python)
- **Flask** - Lightweight web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Session** - Session management
- **Flask-CORS** - Cross-origin resource sharing
- **Werkzeug** - Password hashing utilities
- **psycopg2-binary** - PostgreSQL adapter

### Frontend
- **React 18** - Component-based UI framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Shadcn/UI** - Modern component library
- **React Query** - Server state management
- **Wouter** - Lightweight routing

### Database
- **PostgreSQL** - Relational database
- **SQLAlchemy ORM** - Object-relational mapping

## 📊 Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(10) NOT NULL, -- 'driver' or 'rider'
    rating INTEGER DEFAULT 5,
    total_rides INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Rides table
CREATE TABLE rides (
    id SERIAL PRIMARY KEY,
    driver_id INTEGER REFERENCES users(id),
    origin VARCHAR(200) NOT NULL,
    destination VARCHAR(200) NOT NULL,
    date VARCHAR(20) NOT NULL,
    time VARCHAR(10) NOT NULL,
    available_seats INTEGER NOT NULL,
    price INTEGER NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Ride requests table
CREATE TABLE ride_requests (
    id SERIAL PRIMARY KEY,
    ride_id INTEGER REFERENCES rides(id),
    rider_id INTEGER REFERENCES users(id),
    seats INTEGER NOT NULL,
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🚀 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Rides
- `POST /api/rides` - Create new ride (drivers only)
- `GET /api/rides/search` - Search available rides
- `GET /api/rides/my` - Get driver's posted rides

### Ride Requests
- `POST /api/requests` - Create ride request (riders only)
- `GET /api/requests/my` - Get user's requests
- `PATCH /api/requests/:id` - Update request status (drivers only)

### Data Structures Demo
- `GET /api/data-structures/demo` - View data structures usage statistics

## 🏃‍♂️ Running the Project

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL database

### Installation
1. Install Python dependencies:
   ```bash
   pip install flask flask-sqlalchemy flask-session flask-cors psycopg2-binary python-dotenv werkzeug
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   export DATABASE_URL="your_postgresql_connection_string"
   export SESSION_SECRET="your_secret_key"
   ```

4. Build the frontend:
   ```bash
   npm run build
   ```

5. Start the Flask application:
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
rideshare/
├── app.py                 # Main Flask application
├── run.py                 # Application entry point
├── client/                # React frontend
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Application pages
│   │   ├── hooks/         # Custom React hooks
│   │   └── lib/           # Utility functions
├── dist/                  # Built frontend files
└── README.md              # Project documentation
```

## 🎓 Educational Value

This project demonstrates:
- **Practical Data Structures**: Real-world usage of lists, dictionaries, sets, and classes
- **Algorithm Implementation**: Search algorithms, filtering, and data processing
- **Web Development**: Full-stack application with REST API
- **Database Design**: Relational database modeling with foreign keys
- **Session Management**: User authentication and authorization
- **Modern Frontend**: React with TypeScript and modern UI components

## 🚀 Deployment

### Local Development
- Frontend: React with Vite dev server
- Backend: Flask development server
- Database: Local PostgreSQL or cloud provider

### Production Deployment
- Platform: Any cloud provider (Heroku, Replit, Railway, etc.)
- Frontend: Served as static files by Flask
- Backend: Flask with WSGI server (Gunicorn)
- Database: Cloud PostgreSQL (Neon, AWS RDS, etc.)

## 🤝 Contributing

This is an educational project demonstrating data structures implementation. To extend functionality:

1. Add new data structure examples in the `RideShareDataStructures` class
2. Implement additional algorithms for route optimization
3. Add real-time features using WebSockets
4. Integrate mapping services for route visualization

## 📚 Learning Outcomes

Students will learn:
- Python data structures and their time complexities
- Web API design and implementation
- Database relationships and queries
- Frontend-backend integration
- User authentication and session management
- Real-world software development practices

---

**Built with ❤️ for Data Structures & Algorithms Learning**