#!/usr/bin/env python3
"""
Entry point for the RideShare Flask application
"""

if __name__ == '__main__':
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=True)