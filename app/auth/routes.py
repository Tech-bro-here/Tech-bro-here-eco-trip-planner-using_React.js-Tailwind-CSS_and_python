from flask import jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app.models.user import User, Itinerary
from app import db

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {'id': user.id, 'username': user.username, 'email': user.email}
    })

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        login_user(user, remember=data.get('remember', False))
        return jsonify({
            'message': 'Logged in successfully',
            'user': {'id': user.id, 'username': user.username, 'email': user.email}
        })
    
    return jsonify({'error': 'Invalid username or password'}), 401

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'itineraries': [
            {
                'id': itinerary.id,
                'name': itinerary.name,
                'created_at': itinerary.created_at.isoformat(),
                'hotspots_count': len(itinerary.hotspots)
            }
            for itinerary in current_user.itineraries
        ]
    })

@bp.route('/itineraries', methods=['GET'])
@login_required
def get_itineraries():
    return jsonify({
        'itineraries': [
            {
                'id': itinerary.id,
                'name': itinerary.name,
                'created_at': itinerary.created_at.isoformat(),
                'hotspots': itinerary.hotspots
            }
            for itinerary in current_user.itineraries
        ]
    })

@bp.route('/itineraries', methods=['POST'])
@login_required
def create_itinerary():
    data = request.get_json()
    
    itinerary = Itinerary(
        name=data['name'],
        user_id=current_user.id,
        hotspots=data['hotspots']
    )
    
    db.session.add(itinerary)
    db.session.commit()
    
    return jsonify({
        'message': 'Itinerary created successfully',
        'itinerary': {
            'id': itinerary.id,
            'name': itinerary.name,
            'created_at': itinerary.created_at.isoformat(),
            'hotspots': itinerary.hotspots
        }
    })

@bp.route('/me', methods=['GET'])
def me():
    if current_user.is_authenticated:
        return jsonify({
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email
            }
        })
    return jsonify({'user': None}), 401 