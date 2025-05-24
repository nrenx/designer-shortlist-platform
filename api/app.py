from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_cors import CORS
import os
import sqlite3
import json
from datetime import datetime
from decimal import Decimal
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.secret_key = 'emptycup_secret_key_2024'  # For flash messages

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///emptycup.db')
USE_SQLITE = DATABASE_URL.startswith('sqlite')

if not USE_SQLITE:
    import psycopg2
    from psycopg2.extras import RealDictCursor

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_designer_data(data):
    """Validate designer data structure"""
    required_fields = ['name', 'rating', 'description', 'projects', 'experience',
                      'price_range', 'phone1', 'phone2', 'location', 'specialties', 'portfolio']

    errors = []

    for field in required_fields:
        if field not in data:
            errors.append(f'Missing required field: {field}')

    if 'rating' in data:
        try:
            rating = float(data['rating'])
            if not (1.0 <= rating <= 5.0):
                errors.append('Rating must be between 1.0 and 5.0')
        except (ValueError, TypeError):
            errors.append('Rating must be a valid number')

    if 'price_range' in data and data['price_range'] not in ['$', '$$', '$$$']:
        errors.append('Price range must be $, $$, or $$$')

    if 'specialties' in data and not isinstance(data['specialties'], list):
        errors.append('Specialties must be an array')

    if 'portfolio' in data and not isinstance(data['portfolio'], list):
        errors.append('Portfolio must be an array')

    return errors

def execute_query(cursor, query, params=None):
    """Execute query with appropriate parameter style"""
    if USE_SQLITE:
        # Convert %s to ? for SQLite
        sqlite_query = query.replace('%s', '?')
        if params:
            cursor.execute(sqlite_query, params)
        else:
            cursor.execute(sqlite_query)
    else:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

def get_db_connection():
    """Get database connection"""
    try:
        if USE_SQLITE:
            db_path = DATABASE_URL.replace('sqlite:///', '')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
            return conn
        else:
            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
            return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize database with sample data"""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()

        # Create designers table
        if USE_SQLITE:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS designers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    rating REAL NOT NULL,
                    description TEXT NOT NULL,
                    projects INTEGER NOT NULL,
                    experience INTEGER NOT NULL,
                    price_range TEXT NOT NULL,
                    phone1 TEXT NOT NULL,
                    phone2 TEXT NOT NULL,
                    location TEXT NOT NULL,
                    specialties TEXT NOT NULL,
                    portfolio TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        else:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS designers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    rating DECIMAL(2,1) NOT NULL,
                    description TEXT NOT NULL,
                    projects INTEGER NOT NULL,
                    experience INTEGER NOT NULL,
                    price_range VARCHAR(10) NOT NULL,
                    phone1 VARCHAR(20) NOT NULL,
                    phone2 VARCHAR(20) NOT NULL,
                    location VARCHAR(100) NOT NULL,
                    specialties JSONB NOT NULL,
                    portfolio JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

        # Create shortlists table
        if USE_SQLITE:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS shortlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    designer_id INTEGER REFERENCES designers(id),
                    user_session TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(designer_id, user_session)
                )
            ''')

            # Create reports table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    designer_id INTEGER REFERENCES designers(id),
                    reason TEXT NOT NULL,
                    description TEXT,
                    user_session TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        else:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS shortlists (
                    id SERIAL PRIMARY KEY,
                    designer_id INTEGER REFERENCES designers(id),
                    user_session VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(designer_id, user_session)
                )
            ''')

            # Create reports table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    id SERIAL PRIMARY KEY,
                    designer_id INTEGER REFERENCES designers(id),
                    reason VARCHAR(100) NOT NULL,
                    description TEXT,
                    user_session VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

        # Check if data already exists
        cur.execute('SELECT COUNT(*) as count FROM designers')
        result = cur.fetchone()
        # Both SQLite and PostgreSQL with RealDictCursor return dict-like objects
        count = result['count']

        if count == 0:
            # Insert sample data
            sample_designers = [
                {
                    'name': 'Epic Designs',
                    'rating': 3.5,
                    'description': 'Passionate team of 4 designers working out of Bangalore with an experience of 4 years.',
                    'projects': 57,
                    'experience': 8,
                    'price_range': '$$',
                    'phone1': '+91 - 984532853',
                    'phone2': '+91 - 984532854',
                    'location': 'Bangalore',
                    'specialties': json.dumps(['Residential', 'Commercial', 'Modern']),
                    'portfolio': json.dumps([
                        'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400',
                        'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400',
                        'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400'
                    ])
                },
                {
                    'name': 'Studio - D3',
                    'rating': 4.5,
                    'description': 'Passionate team of 4 designers working out of Bangalore with an experience of 4 years.',
                    'projects': 43,
                    'experience': 6,
                    'price_range': '$$$',
                    'phone1': '+91 - 984532853',
                    'phone2': '+91 - 984532854',
                    'location': 'Bangalore',
                    'specialties': json.dumps(['Luxury', 'Residential', 'Contemporary']),
                    'portfolio': json.dumps([
                        'https://images.unsplash.com/photo-1618221195710-dd6b41faaea8?w=400',
                        'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400',
                        'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400'
                    ])
                },
                {
                    'name': 'House of designs',
                    'rating': 4.0,
                    'description': 'Creative studio specializing in modern and minimalist interior designs with 5 years of experience.',
                    'projects': 32,
                    'experience': 5,
                    'price_range': '$$',
                    'phone1': '+91 - 984532853',
                    'phone2': '+91 - 984532854',
                    'location': 'Mumbai',
                    'specialties': json.dumps(['Minimalist', 'Modern', 'Residential']),
                    'portfolio': json.dumps([
                        'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400',
                        'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400',
                        'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400'
                    ])
                }
            ]

            for designer in sample_designers:
                if USE_SQLITE:
                    cur.execute('''
                        INSERT INTO designers (name, rating, description, projects, experience,
                                             price_range, phone1, phone2, location, specialties, portfolio)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (designer['name'], designer['rating'], designer['description'],
                          designer['projects'], designer['experience'], designer['price_range'],
                          designer['phone1'], designer['phone2'], designer['location'],
                          designer['specialties'], designer['portfolio']))
                else:
                    # For PostgreSQL, convert JSON strings to actual JSON objects
                    designer_copy = designer.copy()
                    designer_copy['specialties'] = json.loads(designer['specialties'])
                    designer_copy['portfolio'] = json.loads(designer['portfolio'])

                    cur.execute('''
                        INSERT INTO designers (name, rating, description, projects, experience,
                                             price_range, phone1, phone2, location, specialties, portfolio)
                        VALUES (%(name)s, %(rating)s, %(description)s, %(projects)s, %(experience)s,
                               %(price_range)s, %(phone1)s, %(phone2)s, %(location)s, %(specialties)s, %(portfolio)s)
                    ''', designer_copy)

        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Database initialization error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

@app.route('/', methods=['GET'])
def admin_dashboard():
    """Admin dashboard for managing designers"""
    # Get current designers count using the same logic as the working API endpoint
    conn = get_db_connection()
    designer_count = 0
    recent_designers = []

    if not conn:
        return render_template('admin_dashboard.html',
                             designer_count=designer_count,
                             recent_designers=recent_designers)

    try:
        cur = conn.cursor()

        # Use the same query pattern as the working API endpoint
        cur.execute('SELECT COUNT(*) as count FROM designers')
        result = cur.fetchone()
        designer_count = result['count']

        # Get recent designers
        cur.execute('''
            SELECT id, name, rating, location, created_at
            FROM designers
            ORDER BY id DESC
            LIMIT 5
        ''')
        recent_designers = cur.fetchall()

        cur.close()
        conn.close()

    except Exception as e:
        if conn:
            conn.close()

    return render_template('admin_dashboard.html',
                         designer_count=designer_count,
                         recent_designers=recent_designers)

@app.route('/api/info', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        'message': 'EmptyCup Designer Shortlist API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'designers': '/api/designers',
            'designer_detail': '/api/designers/{id}',
            'shortlist': '/api/designers/{id}/shortlist',
            'report': '/api/designers/{id}/report'
        },
        'admin_interface': '/',
        'documentation': 'See README.md for full API documentation'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'EmptyCup API is running'})



@app.route('/api/designers', methods=['GET'])
def get_designers():
    """Get all designers"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()
        cur.execute('''
            SELECT id, name, rating, description, projects, experience,
                   price_range, phone1, phone2, location,
                   specialties, portfolio
            FROM designers
            ORDER BY experience DESC
        ''')

        designers = cur.fetchall()

        # Convert to list of dictionaries and parse JSON fields
        result = []
        for designer in designers:
            designer_dict = dict(designer)
            # Add priceRange alias for frontend compatibility
            designer_dict['priceRange'] = designer_dict['price_range']
            # Convert Decimal to float for JSON serialization
            if isinstance(designer_dict.get('rating'), Decimal):
                designer_dict['rating'] = float(designer_dict['rating'])
            # Handle JSON fields based on database type
            if USE_SQLITE:
                designer_dict['specialties'] = json.loads(designer_dict['specialties'])
                designer_dict['portfolio'] = json.loads(designer_dict['portfolio'])
            else:
                # PostgreSQL JSONB fields are already parsed
                pass
            result.append(designer_dict)

        cur.close()
        conn.close()

        return jsonify(result)

    except Exception as e:
        print(f"Error fetching designers: {e}")
        if conn:
            conn.close()
        return jsonify({'error': 'Failed to fetch designers'}), 500

@app.route('/api/designers', methods=['POST'])
def add_designer():
    """Add a new designer"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'rating', 'description', 'projects', 'experience',
                      'price_range', 'phone1', 'phone2', 'location', 'specialties', 'portfolio']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()

        # Convert arrays to JSON strings
        specialties_json = json.dumps(data['specialties']) if isinstance(data['specialties'], list) else data['specialties']
        portfolio_json = json.dumps(data['portfolio']) if isinstance(data['portfolio'], list) else data['portfolio']

        if USE_SQLITE:
            cur.execute('''
                INSERT INTO designers (name, rating, description, projects, experience,
                                     price_range, phone1, phone2, location, specialties, portfolio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data['name'], data['rating'], data['description'],
                  data['projects'], data['experience'], data['price_range'],
                  data['phone1'], data['phone2'], data['location'],
                  specialties_json, portfolio_json))
        else:
            cur.execute('''
                INSERT INTO designers (name, rating, description, projects, experience,
                                     price_range, phone1, phone2, location, specialties, portfolio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (data['name'], data['rating'], data['description'],
                  data['projects'], data['experience'], data['price_range'],
                  data['phone1'], data['phone2'], data['location'],
                  specialties_json, portfolio_json))

        conn.commit()

        # Get the ID of the newly inserted designer
        if USE_SQLITE:
            designer_id = cur.lastrowid
        else:
            cur.execute('SELECT LASTVAL()')
            result = cur.fetchone()
            designer_id = result['lastval']

        cur.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Designer added successfully',
            'designer_id': designer_id
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({'error': 'Failed to add designer'}), 500

@app.route('/api/designers/<int:designer_id>', methods=['GET'])
def get_designer(designer_id):
    """Get specific designer by ID"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()
        execute_query(cur, '''
            SELECT id, name, rating, description, projects, experience,
                   price_range, phone1, phone2, location,
                   specialties, portfolio
            FROM designers
            WHERE id = %s
        ''', (designer_id,))

        designer = cur.fetchone()

        if not designer:
            cur.close()
            conn.close()
            return jsonify({'error': 'Designer not found'}), 404

        # Convert to dictionary and parse JSON fields
        designer_dict = dict(designer)
        # Add priceRange alias for frontend compatibility
        designer_dict['priceRange'] = designer_dict['price_range']
        # Convert Decimal to float for JSON serialization
        if isinstance(designer_dict.get('rating'), Decimal):
            designer_dict['rating'] = float(designer_dict['rating'])
        # Handle JSON fields based on database type
        if USE_SQLITE:
            designer_dict['specialties'] = json.loads(designer_dict['specialties'])
            designer_dict['portfolio'] = json.loads(designer_dict['portfolio'])
        else:
            # PostgreSQL JSONB fields are already parsed
            pass

        cur.close()
        conn.close()

        return jsonify(designer_dict)

    except Exception as e:
        print(f"Error fetching designer: {e}")
        if conn:
            conn.close()
        return jsonify({'error': 'Failed to fetch designer'}), 500

@app.route('/api/designers/<int:designer_id>/shortlist', methods=['POST'])
def toggle_shortlist(designer_id):
    """Toggle shortlist for a designer"""
    data = request.get_json()
    user_session = data.get('user_session', 'default_session')

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()

        # Check if already shortlisted
        execute_query(cur, '''
            SELECT id FROM shortlists
            WHERE designer_id = %s AND user_session = %s
        ''', (designer_id, user_session))

        existing = cur.fetchone()

        if existing:
            # Remove from shortlist
            execute_query(cur, '''
                DELETE FROM shortlists
                WHERE designer_id = %s AND user_session = %s
            ''', (designer_id, user_session))
            shortlisted = False
        else:
            # Add to shortlist
            execute_query(cur, '''
                INSERT INTO shortlists (designer_id, user_session)
                VALUES (%s, %s)
            ''', (designer_id, user_session))
            shortlisted = True

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            'success': True,
            'shortlisted': shortlisted,
            'designer_id': designer_id
        })

    except Exception as e:
        print(f"Error toggling shortlist: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({'error': 'Failed to toggle shortlist'}), 500

@app.route('/api/designers/<int:designer_id>/report', methods=['POST'])
def report_designer(designer_id):
    """Report a designer"""
    data = request.get_json()
    reason = data.get('reason', '')
    description = data.get('description', '')
    user_session = data.get('user_session', 'default_session')

    if not reason:
        return jsonify({'error': 'Reason is required'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()

        execute_query(cur, '''
            INSERT INTO reports (designer_id, reason, description, user_session)
            VALUES (%s, %s, %s, %s)
        ''', (designer_id, reason, description, user_session))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Report submitted successfully'
        })

    except Exception as e:
        print(f"Error submitting report: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({'error': 'Failed to submit report'}), 500

@app.route('/api/designers/<int:designer_id>', methods=['DELETE'])
def delete_designer(designer_id):
    """Delete a designer and all related records"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor()

        # First check if designer exists
        execute_query(cur, 'SELECT id FROM designers WHERE id = %s', (designer_id,))
        designer = cur.fetchone()

        if not designer:
            cur.close()
            conn.close()
            return jsonify({'error': 'Designer not found'}), 404

        # Delete related records first (to maintain referential integrity)
        # Delete shortlists
        execute_query(cur, 'DELETE FROM shortlists WHERE designer_id = %s', (designer_id,))

        # Delete reports
        execute_query(cur, 'DELETE FROM reports WHERE designer_id = %s', (designer_id,))

        # Finally delete the designer
        execute_query(cur, 'DELETE FROM designers WHERE id = %s', (designer_id,))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': f'Designer {designer_id} and all related records deleted successfully'
        })

    except Exception as e:
        print(f"Error deleting designer: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({'error': 'Failed to delete designer'}), 500

# Web Interface Routes
@app.route('/add-designer', methods=['GET', 'POST'])
def add_designer_form():
    """Web form to add a designer"""
    if request.method == 'POST':
        # Handle form submission
        try:
            # Get form data
            designer_data = {
                'name': request.form['name'],
                'rating': float(request.form['rating']),
                'description': request.form['description'],
                'projects': int(request.form['projects']),
                'experience': int(request.form['experience']),
                'price_range': request.form['price_range'],
                'phone1': request.form['phone1'],
                'phone2': request.form['phone2'],
                'location': request.form['location'],
                'specialties': [s.strip() for s in request.form['specialties'].split(',') if s.strip()],
                'portfolio': [url.strip() for url in request.form['portfolio'].split(',') if url.strip()]
            }

            # Validate data
            errors = validate_designer_data(designer_data)
            if errors:
                flash(f'Validation errors: {", ".join(errors)}', 'error')
                return render_template('add_designer.html', form_data=request.form)

            # Add to database
            conn = get_db_connection()
            if not conn:
                flash('Database connection failed', 'error')
                return render_template('add_designer.html', form_data=request.form)

            cur = conn.cursor()
            specialties_json = json.dumps(designer_data['specialties'])
            portfolio_json = json.dumps(designer_data['portfolio'])

            if USE_SQLITE:
                cur.execute('''
                    INSERT INTO designers (name, rating, description, projects, experience,
                                         price_range, phone1, phone2, location, specialties, portfolio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (designer_data['name'], designer_data['rating'], designer_data['description'],
                      designer_data['projects'], designer_data['experience'], designer_data['price_range'],
                      designer_data['phone1'], designer_data['phone2'], designer_data['location'],
                      specialties_json, portfolio_json))
            else:
                cur.execute('''
                    INSERT INTO designers (name, rating, description, projects, experience,
                                         price_range, phone1, phone2, location, specialties, portfolio)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (designer_data['name'], designer_data['rating'], designer_data['description'],
                      designer_data['projects'], designer_data['experience'], designer_data['price_range'],
                      designer_data['phone1'], designer_data['phone2'], designer_data['location'],
                      specialties_json, portfolio_json))

            conn.commit()

            # Get the ID of the newly inserted designer
            if USE_SQLITE:
                designer_id = cur.lastrowid
            else:
                cur.execute('SELECT LASTVAL()')
                result = cur.fetchone()
                designer_id = result['lastval']

            cur.close()
            conn.close()

            flash(f'Designer "{designer_data["name"]}" added successfully with ID: {designer_id}', 'success')
            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            flash(f'Error adding designer: {str(e)}', 'error')
            return render_template('add_designer.html', form_data=request.form)

    return render_template('add_designer.html')

@app.route('/upload-json', methods=['GET', 'POST'])
def upload_json():
    """Upload designers from JSON file"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            try:
                # Read and parse JSON
                json_data = json.loads(file.read().decode('utf-8'))

                if not isinstance(json_data, list):
                    flash('JSON file must contain an array of designers', 'error')
                    return redirect(request.url)

                # Process each designer
                success_count = 0
                error_count = 0
                errors = []

                conn = get_db_connection()
                if not conn:
                    flash('Database connection failed', 'error')
                    return redirect(request.url)

                for i, designer_data in enumerate(json_data):
                    try:
                        # Validate data
                        validation_errors = validate_designer_data(designer_data)
                        if validation_errors:
                            errors.append(f'Designer {i+1}: {", ".join(validation_errors)}')
                            error_count += 1
                            continue

                        # Add to database
                        cur = conn.cursor()
                        specialties_json = json.dumps(designer_data['specialties'])
                        portfolio_json = json.dumps(designer_data['portfolio'])

                        if USE_SQLITE:
                            cur.execute('''
                                INSERT INTO designers (name, rating, description, projects, experience,
                                                     price_range, phone1, phone2, location, specialties, portfolio)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (designer_data['name'], designer_data['rating'], designer_data['description'],
                                  designer_data['projects'], designer_data['experience'], designer_data['price_range'],
                                  designer_data['phone1'], designer_data['phone2'], designer_data['location'],
                                  specialties_json, portfolio_json))
                        else:
                            cur.execute('''
                                INSERT INTO designers (name, rating, description, projects, experience,
                                                     price_range, phone1, phone2, location, specialties, portfolio)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ''', (designer_data['name'], designer_data['rating'], designer_data['description'],
                                  designer_data['projects'], designer_data['experience'], designer_data['price_range'],
                                  designer_data['phone1'], designer_data['phone2'], designer_data['location'],
                                  specialties_json, portfolio_json))

                        conn.commit()
                        cur.close()
                        success_count += 1

                    except Exception as e:
                        errors.append(f'Designer {i+1} ({designer_data.get("name", "Unknown")}): {str(e)}')
                        error_count += 1

                conn.close()

                # Show results
                if success_count > 0:
                    flash(f'Successfully added {success_count} designers', 'success')
                if error_count > 0:
                    flash(f'Failed to add {error_count} designers. Errors: {"; ".join(errors[:5])}', 'error')

                return redirect(url_for('admin_dashboard'))

            except json.JSONDecodeError:
                flash('Invalid JSON file format', 'error')
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'error')
        else:
            flash('Invalid file type. Please upload a JSON file.', 'error')

    return render_template('upload_json.html')

@app.route('/designers-list')
def designers_list():
    """View all designers in web interface"""
    conn = get_db_connection()
    designers = []

    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                SELECT id, name, rating, description, projects, experience,
                       price_range, phone1, phone2, location, specialties, portfolio,
                       created_at
                FROM designers
                ORDER BY created_at DESC
            ''')
            designers_raw = cur.fetchall()

            # Parse JSON fields based on database type
            for designer in designers_raw:
                designer_dict = dict(designer)
                # Handle JSON fields based on database type
                if USE_SQLITE:
                    designer_dict['specialties'] = json.loads(designer_dict['specialties'])
                    designer_dict['portfolio'] = json.loads(designer_dict['portfolio'])
                else:
                    # PostgreSQL JSONB fields are already parsed
                    pass
                designers.append(designer_dict)

            cur.close()
            conn.close()
        except Exception as e:
            flash(f'Error fetching designers: {str(e)}', 'error')
            if conn:
                conn.close()

    return render_template('designers_list.html', designers=designers)

@app.route('/delete-designer/<int:designer_id>', methods=['POST'])
def delete_designer_web(designer_id):
    """Delete designer via web interface"""
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('designers_list'))

    try:
        cur = conn.cursor()

        # Get designer name for confirmation message
        execute_query(cur, 'SELECT name FROM designers WHERE id = %s', (designer_id,))
        designer = cur.fetchone()

        if not designer:
            flash('Designer not found', 'error')
            return redirect(url_for('designers_list'))

        # Both SQLite and PostgreSQL with RealDictCursor return dict-like objects
        designer_name = designer['name']

        # Delete related records first
        execute_query(cur, 'DELETE FROM shortlists WHERE designer_id = %s', (designer_id,))
        execute_query(cur, 'DELETE FROM reports WHERE designer_id = %s', (designer_id,))

        # Delete the designer
        execute_query(cur, 'DELETE FROM designers WHERE id = %s', (designer_id,))

        conn.commit()
        cur.close()
        conn.close()

        flash(f'Designer "{designer_name}" deleted successfully', 'success')

    except Exception as e:
        print(f"Error deleting designer: {e}")
        if conn:
            conn.rollback()
            conn.close()
        flash(f'Error deleting designer: {str(e)}', 'error')

    return redirect(url_for('designers_list'))

if __name__ == '__main__':
    # Initialize database on startup
    init_database()

    port = int(os.environ.get('PORT', 5001))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
