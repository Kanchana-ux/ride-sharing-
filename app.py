import os
from flask import Flask, request, jsonify, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app with static files
app = Flask(__name__, static_folder='dist/public', static_url_path='')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'rideshare-secret-key')
# Use default SQLite database if DATABASE_URL is not set
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///rideshare.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

# Initialize extensions
db = SQLAlchemy(app)
Session(app)
CORS(app, supports_credentials=True)

# Models
class User(db.Model):
    """User model representing both drivers and riders"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'driver' or 'rider'
    rating = db.Column(db.Integer, default=5)
    total_rides = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    rides_as_driver = db.relationship('Ride', backref='driver', lazy=True)
    ride_requests = db.relationship('RideRequest', backref='rider', lazy=True)
    
    def to_dict(self):
        """Convert user object to dictionary (excluding password)"""
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'rating': self.rating,
            'totalRides': self.total_rides,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

class Ride(db.Model):
    """Ride model representing ride offers from drivers"""
    __tablename__ = 'rides'
    
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    origin = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    requests = db.relationship('RideRequest', backref='ride', lazy=True)
    
    def to_dict(self, include_driver=False):
        """Convert ride object to dictionary"""
        result = {
            'id': self.id,
            'driverId': self.driver_id,
            'origin': self.origin,
            'destination': self.destination,
            'date': self.date,
            'time': self.time,
            'availableSeats': self.available_seats,
            'price': self.price,
            'vehicleType': self.vehicle_type,
            'notes': self.notes,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_driver:
            driver = User.query.get(self.driver_id)
            if driver:
                result['driver'] = driver.to_dict()
            
        return result

class RideRequest(db.Model):
    """Ride request model representing requests from riders to join rides"""
    __tablename__ = 'ride_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.id'), nullable=False)
    rider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'declined'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self, include_rider=False, include_ride=False):
        """Convert ride request object to dictionary"""
        result = {
            'id': self.id,
            'rideId': self.ride_id,
            'riderId': self.rider_id,
            'seats': self.seats,
            'message': self.message,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_rider:
            rider = User.query.get(self.rider_id)
            if rider:
                result['rider'] = rider.to_dict()
            
        if include_ride:
            ride = Ride.query.get(self.ride_id)
            if ride:
                result['ride'] = ride.to_dict(include_driver=True)
            
        return result

# Data Structure Classes demonstrating Python data structures usage
class RideShareDataStructures:
    """Class demonstrating various Python data structures for ride sharing"""
    
    def __init__(self):
        # List: For storing collections of data with order
        self.active_rides = []  # List of active ride IDs
        self.search_history = []  # List of recent searches
        
        # Dictionary: For fast lookups and key-value mapping
        self.user_sessions = {}  # {user_id: session_data}
        self.ride_cache = {}  # {ride_id: ride_data}
        self.driver_rides = {}  # {driver_id: [ride_ids]}
        
        # Set: For ensuring uniqueness and fast membership testing
        self.unique_emails = set()  # Set of registered emails
        self.active_drivers = set()  # Set of currently active driver IDs
        self.blocked_users = set()  # Set of blocked user IDs
        
        # Tuple: For immutable coordinate pairs and grouped data
        self.popular_routes = [
            ("Mumbai Central", "Bandra"),
            ("Pune Station", "Hadapsar"),
            ("Delhi CP", "Gurgaon")
        ]
        
    def add_user_email(self, email):
        """Add email to unique set (demonstrates set usage)"""
        if email in self.unique_emails:
            return False  # Email already exists
        self.unique_emails.add(email)
        return True
        
    def cache_ride(self, ride_id, ride_data):
        """Cache ride data (demonstrates dictionary usage)"""
        self.ride_cache[ride_id] = ride_data
        
    def add_to_search_history(self, search_params):
        """Add search to history (demonstrates list usage)"""
        # Keep only last 10 searches
        if len(self.search_history) >= 10:
            self.search_history.pop(0)  # Remove oldest
        self.search_history.append(search_params)
        
    def get_popular_route_suggestions(self, origin):
        """Get route suggestions (demonstrates tuple usage)"""
        suggestions = []
        for route_origin, route_dest in self.popular_routes:
            if route_origin.lower() == origin.lower():
                suggestions.append(route_dest)
        return suggestions

# Initialize data structures
ride_data = RideShareDataStructures()

# Authentication helper
def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'phone', 'password', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing field: {field}'}), 400
        
        # Check if email already exists using our data structure
        if not ride_data.add_user_email(data['email']):
            return jsonify({'message': 'Email already registered'}), 400
            
        # Check if user exists in database
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400
        
        # Create new user
        user = User(
            first_name=data['firstName'],
            last_name=data['lastName'],
            email=data['email'],
            phone=data['phone'],
            password_hash=generate_password_hash(data['password']),
            role=data['role']
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create session
        session['user_id'] = user.id
        session['user_role'] = user.role
        
        # Cache user session data
        ride_data.user_sessions[user.id] = {
            'role': user.role,
            'email': user.email,
            'login_time': datetime.now().isoformat()
        }
        
        return jsonify(user.to_dict()), 201
        
    except Exception as e:
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Email and password required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            session['user_id'] = user.id
            session['user_role'] = user.role
            
            # Cache user session data
            ride_data.user_sessions[user.id] = {
                'role': user.role,
                'email': user.email,
                'login_time': datetime.now().isoformat()
            }
            
            # Add to active drivers set if driver
            if user.role == 'driver':
                ride_data.active_drivers.add(user.id)
            
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        user_id = session.get('user_id')
        
        # Remove from active drivers if driver
        if user_id and user_id in ride_data.active_drivers:
            ride_data.active_drivers.remove(user_id)
            
        # Clear session data
        if user_id and user_id in ride_data.user_sessions:
            del ride_data.user_sessions[user_id]
            
        session.clear()
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': 'Logout failed', 'error': str(e)}), 500

@app.route('/api/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user data"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'message': 'User not found'}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get user', 'error': str(e)}), 500

@app.route('/api/rides', methods=['POST'])
@require_auth
def create_ride():
    """Create a new ride (drivers only)"""
    try:
        if session.get('user_role') != 'driver':
            return jsonify({'message': 'Only drivers can post rides'}), 403
            
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['origin', 'destination', 'date', 'time', 'availableSeats', 'price', 'vehicleType']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing field: {field}'}), 400
        
        ride = Ride(
            driver_id=session['user_id'],
            origin=data['origin'],
            destination=data['destination'],
            date=data['date'],
            time=data['time'],
            available_seats=data['availableSeats'],
            price=data['price'],
            vehicle_type=data['vehicleType'],
            notes=data.get('notes', '')
        )
        
        db.session.add(ride)
        db.session.commit()
        
        # Add to active rides list
        ride_data.active_rides.append(ride.id)
        
        # Cache ride data
        ride_data.cache_ride(ride.id, ride.to_dict())
        
        # Update driver rides mapping
        driver_id = session['user_id']
        if driver_id not in ride_data.driver_rides:
            ride_data.driver_rides[driver_id] = []
        ride_data.driver_rides[driver_id].append(ride.id)
        
        return jsonify(ride.to_dict()), 201
        
    except Exception as e:
        return jsonify({'message': 'Failed to create ride', 'error': str(e)}), 500

@app.route('/api/rides/search', methods=['GET'])
def search_rides():
    """Search for available rides"""
    try:
        # Get search parameters
        origin = request.args.get('origin', '')
        destination = request.args.get('destination', '')
        date = request.args.get('date', '')
        
        # Add to search history (demonstrating list usage)
        search_params = {
            'origin': origin,
            'destination': destination,
            'date': date,
            'timestamp': datetime.now().isoformat()
        }
        ride_data.add_to_search_history(search_params)
        
        # Build query
        query = Ride.query.filter_by(status='active')
        
        if origin:
            query = query.filter(Ride.origin.ilike(f'%{origin}%'))
        if destination:
            query = query.filter(Ride.destination.ilike(f'%{destination}%'))
        if date:
            query = query.filter_by(date=date)
            
        rides = query.order_by(Ride.created_at.desc()).all()
        
        # Convert to list of dictionaries with driver info
        result = []
        for ride in rides:
            ride_dict = ride.to_dict(include_driver=True)
            result.append(ride_dict)
            
            # Cache each ride
            ride_data.cache_ride(ride.id, ride_dict)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'message': 'Search failed', 'error': str(e)}), 500

@app.route('/api/rides/my', methods=['GET'])
@require_auth
def get_my_rides():
    """Get rides posted by the current driver"""
    try:
        if session.get('user_role') != 'driver':
            return jsonify({'message': 'Only drivers can view posted rides'}), 403
            
        rides = Ride.query.filter_by(driver_id=session['user_id']).order_by(Ride.created_at.desc()).all()
        result = [ride.to_dict() for ride in rides]
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to get rides', 'error': str(e)}), 500

@app.route('/api/requests', methods=['POST'])
@require_auth
def create_ride_request():
    """Create a ride request (riders only)"""
    try:
        if session.get('user_role') != 'rider':
            return jsonify({'message': 'Only riders can request rides'}), 403
            
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['rideId', 'seats']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing field: {field}'}), 400
        
        # Check if ride exists and has available seats
        ride = Ride.query.get(data['rideId'])
        if not ride:
            return jsonify({'message': 'Ride not found'}), 404
            
        if ride.available_seats < data['seats']:
            return jsonify({'message': 'Not enough available seats'}), 400
        
        # Create ride request
        ride_request = RideRequest(
            ride_id=data['rideId'],
            rider_id=session['user_id'],
            seats=data['seats'],
            message=data.get('message', '')
        )
        
        db.session.add(ride_request)
        db.session.commit()
        
        return jsonify(ride_request.to_dict()), 201
        
    except Exception as e:
        return jsonify({'message': 'Failed to create request', 'error': str(e)}), 500

@app.route('/api/requests/my', methods=['GET'])
@require_auth
def get_my_requests():
    """Get requests based on user role"""
    try:
        user_role = session.get('user_role')
        user_id = session['user_id']
        
        if user_role == 'driver':
            # Get requests for driver's rides
            requests = db.session.query(RideRequest).join(Ride).filter(
                Ride.driver_id == user_id
            ).order_by(RideRequest.created_at.desc()).all()
            
            result = []
            for req in requests:
                req_dict = req.to_dict(include_rider=True)
                req_dict['ride'] = req.ride.to_dict()
                result.append(req_dict)
                
        else:  # rider
            # Get requests made by rider
            requests = RideRequest.query.filter_by(rider_id=user_id).order_by(RideRequest.created_at.desc()).all()
            result = [req.to_dict(include_ride=True) for req in requests]
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to get requests', 'error': str(e)}), 500

@app.route('/api/requests/<int:request_id>', methods=['PATCH'])
@require_auth
def update_request_status(request_id):
    """Update ride request status (drivers only)"""
    try:
        if session.get('user_role') != 'driver':
            return jsonify({'message': 'Only drivers can update request status'}), 403
            
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['accepted', 'declined']:
            return jsonify({'message': 'Invalid status'}), 400
        
        ride_request = RideRequest.query.get(request_id)
        if not ride_request:
            return jsonify({'message': 'Request not found'}), 404
            
        # Get the ride and verify the driver owns it
        ride = Ride.query.get(ride_request.ride_id)
        if not ride or ride.driver_id != session['user_id']:
            return jsonify({'message': 'Unauthorized'}), 403
        
        ride_request.status = status
        
        # If accepted, reduce available seats
        if status == 'accepted':
            ride.available_seats -= ride_request.seats
            
            # Remove from active rides if no seats left
            if ride.available_seats <= 0 and ride.id in ride_data.active_rides:
                ride_data.active_rides.remove(ride.id)
        
        db.session.commit()
        
        return jsonify({'message': 'Request updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to update request', 'error': str(e)}), 500

@app.route('/api/data-structures/demo', methods=['GET'])
def demo_data_structures():
    """Demonstrate the data structures being used"""
    return jsonify({
        'message': 'Data Structures Demo',
        'structures': {
            'lists': {
                'active_rides': len(ride_data.active_rides),
                'search_history': len(ride_data.search_history),
                'description': 'Used for ordered collections, easy iteration, dynamic sizing'
            },
            'dictionaries': {
                'user_sessions': len(ride_data.user_sessions),
                'ride_cache': len(ride_data.ride_cache),
                'driver_rides': len(ride_data.driver_rides),
                'description': 'Used for fast O(1) lookups, key-value mapping, caching'
            },
            'sets': {
                'unique_emails': len(ride_data.unique_emails),
                'active_drivers': len(ride_data.active_drivers),
                'blocked_users': len(ride_data.blocked_users),
                'description': 'Used for uniqueness, fast membership testing, no duplicates'
            },
            'tuples': {
                'popular_routes': len(ride_data.popular_routes),
                'description': 'Used for immutable grouped data, coordinate pairs'
            }
        },
        'recent_searches': ride_data.search_history[-3:] if ride_data.search_history else []
    }), 200

# Serve React frontend
@app.route('/')
def serve_frontend():
    """Serve the React frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files or fallback to React app"""
    try:
        return send_from_directory(app.static_folder, path)
    except:
        # Fallback to React app for client-side routing
        return send_from_directory(app.static_folder, 'index.html')

# Create tables and run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        print("Starting Flask application on http://0.0.0.0:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)