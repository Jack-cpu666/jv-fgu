from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import json
import os
import base64
import re
from datetime import datetime, timedelta
import threading
import time
from functools import wraps
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configuration from environment variables
AUTH_KEY = os.environ.get('AUTH_KEY', 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJpbXpVMnE4NXQxSDB5U2RpUHRKNmtmeWpkYXZlR2ZiaHdyZ01KbXNHZTQ4In0.eyJleHAiOjE3NjE0NTMwOTMsImlhdCI6MTc2MTQ0OTQ5MywiYXV0aF90aW1lIjoxNzYxNDQ5NDkyLCJqdGkiOiJlZmI2NzY2ZS04MTFlLTQzMmUtODc0Yy05NDc3YTRhYTIxMGQiLCJpc3MiOiJodHRwczovL2F1dGgubWV0cm9wb2xpcy5pby9yZWFsbXMvbWV0cm9wb2xpcyIsImF1ZCI6WyJtZXRyb3BvbGlzLXJlc291cmNlLWNsaWVudCIsIm1ldHJvcG9saXMtdXNlci1jbGllbnQiLCJtZXRyb3BvbGlzLXNlcnZlci1jbGllbnQiLCJhY2NvdW50Il0sInN1YiI6ImU2MzEzOWI2LWUyNzgtNGUwNS05ZDJmLTMzZWUxOGQwZGI4YyIsInR5cCI6IkJlYXJlciIsImF6cCI6Im1ldHJvcG9saXMtd2ViLWNsaWVudCIsIm5vbmNlIjoiMzA5MzA4MTYtM2JlYS00NTg1LTkyYWEtMzJlMDYwYzBhNjIzIiwic2Vzc2lvbl9zdGF0ZSI6ImQxMDk4YWJlLTM0ZTYtNGQ2Ny1hMTk2LTdlZWI3YTQ4YWRjZSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9tYW5hZ2VyLm1ldHJvcG9saXMuaW8iLCJodHRwczovL3BvcnRhbC5tZXRyb3BvbGlzLmlvIiwiaHR0cHM6Ly9yZXF1ZXN0Lm1ldHJvcG9saXMuaW8iLCJodHRwczovL2ludGFrZS5tZXRyb3BvbGlzLmlvIiwiaHR0cHM6Ly9kZXZvcHMudG9vbHMubWV0cm9wLmlvIiwiaHR0cHM6Ly9oYXJkd2FyZS5lZGdlLm1ldHJvcG9saXMuaW8iLCJodHRwczovL3NwZWNpYWxpc3QubWV0cm9wb2xpcy5pbyIsImh0dHA6Ly9sb2NhbGhvc3Q6MzAwMSIsImh0dHA6Ly9sb2NhbGhvc3Q6MzAwMCIsImh0dHBzOi8vZWRnZS5hdGcubWV0cm9wb2xpcy5pbyJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy10ZXN0Iiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7Im1ldHJvcG9saXMtc2VydmVyLWNsaWVudCI6eyJyb2xlcyI6WyJlbmZvcmNlbWVudCIsInBhcmtpbmcgcGFzcyIsInZhbGV0IiwiaW50YWtlIiwib3BlcmF0b3IiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwic2lkIjoiZDEwOThhYmUtMzRlNi00ZDY3LWExOTYtN2VlYjdhNDhhZGNlIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiI1NTUgU2VjdXJpdHkgIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VjdXJpdHlANTU1Y2FwaXRvbG1hbGwuY29tIiwiZ2l2ZW5fbmFtZSI6IjU1NSIsImZhbWlseV9uYW1lIjoiU2VjdXJpdHkgIiwiZW1haWwiOiJzZWN1cml0eUA1NTVjYXBpdG9sbWFsbC5jb20ifQ.Xcaxd5K_0sazYYyaqDZiKWapPLqkKcrJcr6ox_Uei-PpRNLBRFTcjCuj3EAHTVL1Va0w0WFvY0uVP51PTRnrx8IvZsNpbu38B9BF6a_gjk0oMHSIb8A3Eu-rQsNdniiirDk7Yy_f-7mp6FCa6xIr83rHeyNnwMdTP_EkOzD-fUSgLtUVWmM9JoRDlv9U2A6hM1gVehV3EY5T5PQH4IcHATkeJmCWCA2N5KTjCmTHNVlWyrX84YX6TGmuDIdzJCdb2WHfOIM5Pf6128s-BHDhurB-nF27ktZ7dlbQOUkaCiIUlHzMqdAVqHRJK-eyX0Fd6KBUZa64cuJoanZNRTGldQ')
BASE_URL = os.environ.get('BASE_URL', 'https://specialist.api.metropolis.io')
SITE_ID = os.environ.get('SITE_ID', '4005')
EMAIL = os.environ.get('EMAIL', 'security@555capitolmall.com')
PASSWORD = os.environ.get('PASSWORD', '555_Security')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin555')

# In-memory storage
member_plates = []
blacklist_plates = []
monitoring_active = False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# HTML Template (embedded for single file deployment)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metropolis Parking Management</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #1e88e5;
            --secondary: #00acc1;
            --success: #43a047;
            --danger: #e53935;
            --warning: #fb8c00;
            --dark: #212121;
            --light: #f5f5f5;
            --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        
        .login-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 400px;
            backdrop-filter: blur(10px);
        }
        
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 1rem 0;
        }
        
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5rem;
            color: white!important;
        }
        
        .nav-link {
            color: rgba(255,255,255,0.9)!important;
            margin: 0 10px;
            border-radius: 5px;
            transition: all 0.3s;
        }
        
        .nav-link:hover, .nav-link.active {
            background: rgba(255,255,255,0.2);
            color: white!important;
        }
        
        .main-container {
            background: white;
            min-height: 100vh;
            padding-top: 70px;
        }
        
        .dashboard-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            margin-bottom: 25px;
        }
        
        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .btn-custom {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn-custom:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            color: white;
        }
        
        .gate-btn {
            width: 100%;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            font-size: 1.2rem;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .gate-btn.entry {
            background: linear-gradient(135deg, #00c851 0%, #00695c 100%);
            color: white;
            border: none;
        }
        
        .gate-btn.exit {
            background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
            color: white;
            border: none;
        }
        
        .gate-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .table-custom {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }
        
        .table-custom thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .badge-custom {
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: 600;
        }
        
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .camera-feed {
            background: #000;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
            text-align: center;
        }
        
        .camera-feed img {
            max-width: 100%;
            border-radius: 5px;
        }
        
        .alert-custom {
            border-radius: 10px;
            border: none;
            padding: 15px 20px;
        }
        
        .tab-content {
            padding: 30px;
            background: #f8f9fa;
            border-radius: 0 0 15px 15px;
        }
        
        .nav-tabs .nav-link {
            color: #666;
            border: none;
            padding: 15px 25px;
            font-weight: 600;
        }
        
        .nav-tabs .nav-link.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px 10px 0 0;
        }
        
        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        
        .modal-content {
            border-radius: 15px;
        }
        
        .modal-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px 15px 0 0;
        }
        
        @media (max-width: 768px) {
            .dashboard-card {
                margin-bottom: 15px;
            }
            
            .stat-card {
                margin-bottom: 15px;
            }
        }
    </style>
</head>
<body>
    {% if session.get('logged_in') %}
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="fas fa-parking"></i> Metropolis Parking
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/" id="nav-dashboard">
                            <i class="fas fa-tachometer-alt"></i> Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/gates" id="nav-gates">
                            <i class="fas fa-door-open"></i> Gates
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/transactions" id="nav-transactions">
                            <i class="fas fa-receipt"></i> Transactions
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/members" id="nav-members">
                            <i class="fas fa-users"></i> Members
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/visitor" id="nav-visitor">
                            <i class="fas fa-user-plus"></i> Visitor Pass
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/cameras" id="nav-cameras">
                            <i class="fas fa-video"></i> Cameras
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/logout">
                            <i class="fas fa-sign-out-alt"></i> Logout
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="main-container">
        <div class="container-fluid pt-4">
            {% block content %}{% endblock %}
        </div>
    </div>
    {% else %}
    <!-- Login Page -->
    <div class="login-container">
        <div class="login-card">
            <h2 class="text-center mb-4">
                <i class="fas fa-parking" style="color: #667eea;"></i>
                <br>
                Metropolis Parking
            </h2>
            <form method="POST" action="/login">
                <div class="mb-3">
                    <label class="form-label">Password</label>
                    <input type="password" class="form-control" name="password" required>
                </div>
                <button type="submit" class="btn btn-custom w-100">
                    <i class="fas fa-sign-in-alt"></i> Login
                </button>
            </form>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else category }} mt-3">
                        {{ message }}
                    </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>
    </div>
    {% endif %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        // Set active nav item
        $(document).ready(function() {
            const path = window.location.pathname;
            $('.nav-link').removeClass('active');
            if (path === '/') {
                $('#nav-dashboard').addClass('active');
            } else if (path.includes('gates')) {
                $('#nav-gates').addClass('active');
            } else if (path.includes('transactions')) {
                $('#nav-transactions').addClass('active');
            } else if (path.includes('members')) {
                $('#nav-members').addClass('active');
            } else if (path.includes('visitor')) {
                $('#nav-visitor').addClass('active');
            } else if (path.includes('cameras')) {
                $('#nav-cameras').addClass('active');
            }
        });

        // Auto-refresh functions
        function autoRefresh(elementId, url, interval) {
            function refresh() {
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById(elementId).innerHTML = data.html || JSON.stringify(data, null, 2);
                    })
                    .catch(error => console.error('Error:', error));
            }
            refresh();
            setInterval(refresh, interval);
        }

        // Gate control
        function openGate(laneId, gateName, siteId) {
            if (!confirm(`Open ${gateName}?`)) return;
            
            fetch('/api/open-gate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    lane_id: laneId,
                    gate_name: gateName,
                    site_id: siteId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`${gateName} opened successfully!`);
                } else {
                    alert(`Error: ${data.message}`);
                }
            })
            .catch(error => {
                alert(`Error: ${error}`);
            });
        }

        // Member management
        function addMember() {
            const plate = document.getElementById('member-plate').value.trim().toUpperCase();
            if (!plate) return;
            
            fetch('/api/members/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({plate: plate})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.message);
                }
            });
        }

        function removeMember(plate) {
            if (!confirm(`Remove ${plate} from members?`)) return;
            
            fetch('/api/members/remove', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({plate: plate})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        }

        // Blacklist management
        function addBlacklist() {
            const plate = document.getElementById('blacklist-plate').value.trim().toUpperCase();
            const reason = document.getElementById('blacklist-reason').value.trim();
            if (!plate) return;
            
            fetch('/api/blacklist/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({plate: plate, reason: reason})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.message);
                }
            });
        }

        function removeBlacklist(plate) {
            if (!confirm(`Remove ${plate} from blacklist?`)) return;
            
            fetch('/api/blacklist/remove', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({plate: plate})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        }

        // Create visitor pass
        function createVisitorPass() {
            const plate = document.getElementById('visitor-plate').value.trim().toUpperCase();
            const hours = document.getElementById('visitor-hours').value;
            const siteId = document.getElementById('visitor-site').value;
            
            if (!plate || !hours) {
                alert('Please fill all fields');
                return;
            }
            
            fetch('/api/visitor-pass', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    plate: plate,
                    hours: hours,
                    site_id: siteId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('visitor-result').innerHTML = `
                        <div class="alert alert-success">
                            <h5>Visitor Pass Created!</h5>
                            <p>Plate: ${data.plate}</p>
                            <p>Valid until: ${data.valid_until}</p>
                            <p>Site: ${data.site}</p>
                        </div>
                    `;
                } else {
                    alert(`Error: ${data.message}`);
                }
            });
        }
    </script>
</body>
</html>
'''

# Routes
@app.route('/')
@login_required
def dashboard():
    return render_template_string(HTML_TEMPLATE + '''
    {% block content %}
    <div class="row">
        <div class="col-12">
            <h1 class="mb-4">Dashboard</h1>
        </div>
    </div>
    
    <div class="row">
        <!-- Statistics -->
        <div class="col-md-3 col-sm-6">
            <div class="stat-card">
                <i class="fas fa-car fa-3x mb-3"></i>
                <div class="stat-number" id="occupancy-555">--</div>
                <div>555 Capitol Occupancy</div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <i class="fas fa-car fa-3x mb-3"></i>
                <div class="stat-number" id="occupancy-boa">--</div>
                <div>Bank of America Occupancy</div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <i class="fas fa-clock fa-3x mb-3"></i>
                <div class="stat-number" id="waiting-count">--</div>
                <div>Cars Waiting at Exit</div>
            </div>
        </div>
        <div class="col-md-3 col-sm-6">
            <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <i class="fas fa-users fa-3x mb-3"></i>
                <div class="stat-number">{{ member_count }}</div>
                <div>Active Members</div>
            </div>
        </div>
    </div>
    
    <div class="row mt-4">
        <!-- Recent Transactions -->
        <div class="col-md-6">
            <div class="dashboard-card">
                <h3 class="mb-3">
                    <i class="fas fa-receipt"></i> Recent Transactions
                </h3>
                <div id="recent-transactions" style="max-height: 400px; overflow-y: auto;">
                    <div class="text-center">
                        <div class="loading-spinner"></div>
                        <p>Loading...</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Quick Actions -->
        <div class="col-md-6">
            <div class="dashboard-card">
                <h3 class="mb-3">
                    <i class="fas fa-bolt"></i> Quick Actions
                </h3>
                <div class="d-grid gap-2">
                    <a href="/gates" class="btn btn-custom">
                        <i class="fas fa-door-open"></i> Open Gates
                    </a>
                    <a href="/visitor" class="btn btn-custom">
                        <i class="fas fa-user-plus"></i> Create Visitor Pass
                    </a>
                    <a href="/transactions" class="btn btn-custom">
                        <i class="fas fa-search"></i> Search Transactions
                    </a>
                    <a href="/members" class="btn btn-custom">
                        <i class="fas fa-users"></i> Manage Members
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Auto-refresh occupancy
        autoRefresh('occupancy-555', '/api/occupancy/4005', 5000);
        autoRefresh('occupancy-boa', '/api/occupancy/4007', 5000);
        autoRefresh('waiting-count', '/api/waiting-count', 5000);
        autoRefresh('recent-transactions', '/api/recent-transactions', 3000);
    </script>
    {% endblock %}
    ''', member_count=len(member_plates))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(HTML_TEMPLATE, error='Invalid password')
    return render_template_string(HTML_TEMPLATE)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/gates')
@login_required
def gates():
    return render_template_string(HTML_TEMPLATE + '''
    {% block content %}
    <div class="row">
        <div class="col-12">
            <h1 class="mb-4">Gate Control</h1>
        </div>
    </div>
    
    <div class="row">
        <!-- 555 Capitol Mall Gates -->
        <div class="col-md-6">
            <div class="dashboard-card">
                <h3 class="text-center mb-4">555 Capitol Mall</h3>
                <button class="gate-btn entry" onclick="openGate('17491', 'Entry Lane 1 (17491)', '4005')">
                    <i class="fas fa-arrow-down"></i> Entry Lane 1
                </button>
                <button class="gate-btn entry" onclick="openGate('17492', 'Entry Lane 2 (17492)', '4005')">
                    <i class="fas fa-arrow-down"></i> Entry Lane 2
                </button>
                <button class="gate-btn exit" onclick="openGate('17493', 'Exit Lane 3 (17493)', '4005')">
                    <i class="fas fa-arrow-up"></i> Exit Lane 3
                </button>
                <button class="gate-btn exit" onclick="openGate('17494', 'Exit Lane 4 (17494)', '4005')">
                    <i class="fas fa-arrow-up"></i> Exit Lane 4
                </button>
                <button class="gate-btn exit" onclick="openGate('17495', 'Exit Lane 5 (17495)', '4005')">
                    <i class="fas fa-arrow-up"></i> Exit Lane 5
                </button>
            </div>
        </div>
        
        <!-- Bank of America Gates -->
        <div class="col-md-6">
            <div class="dashboard-card">
                <h3 class="text-center mb-4">Bank of America</h3>
                <button class="gate-btn entry" onclick="openGate('21173', 'Entry Lane 1 (21173)', '4007')">
                    <i class="fas fa-arrow-down"></i> Entry Lane 1
                </button>
                <button class="gate-btn entry" onclick="openGate('21174', 'Entry Lane 2 (21174)', '4007')">
                    <i class="fas fa-arrow-down"></i> Entry Lane 2
                </button>
                <button class="gate-btn exit" onclick="openGate('21175', 'Exit Lane 3 (21175)', '4007')">
                    <i class="fas fa-arrow-up"></i> Exit Lane 3
                </button>
                <button class="gate-btn exit" onclick="openGate('21176', 'Exit Lane 4 (21176)', '4007')">
                    <i class="fas fa-arrow-up"></i> Exit Lane 4
                </button>
            </div>
        </div>
    </div>
    
    <div class="row mt-4">
        <div class="col-12">
            <div class="dashboard-card">
                <h3 class="mb-3">Gate Status</h3>
                <div id="gate-status">
                    <p class="text-muted">Click a gate button to open it</p>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    ''')

@app.route('/transactions')
@login_required  
def transactions():
    return render_template_string(HTML_TEMPLATE + '''
    {% block content %}
    <div class="row">
        <div class="col-12">
            <h1 class="mb-4">Transaction Search</h1>
        </div>
    </div>
    
    <div class="dashboard-card">
        <form onsubmit="searchTransactions(event); return false;">
            <div class="row">
                <div class="col-md-4">
                    <label>License Plate</label>
                    <input type="text" class="form-control" id="search-plate" placeholder="Enter plate number">
                </div>
                <div class="col-md-4">
                    <label>Site</label>
                    <select class="form-control" id="search-site">
                        <option value="4005">555 Capitol Mall</option>
                        <option value="4007">Bank of America</option>
                        <option value="all">All Sites</option>
                    </select>
                </div>
                <div class="col-md-4">
                    <label>&nbsp;</label>
                    <button type="submit" class="btn btn-custom w-100">
                        <i class="fas fa-search"></i> Search
                    </button>
                </div>
            </div>
        </form>
    </div>
    
    <div class="dashboard-card mt-4">
        <h3>Search Results</h3>
        <div id="transaction-results" style="max-height: 600px; overflow-y: auto;">
            <p class="text-muted">Enter search criteria above</p>
        </div>
    </div>
    
    <script>
        function searchTransactions(e) {
            e.preventDefault();
            const plate = document.getElementById('search-plate').value;
            const site = document.getElementById('search-site').value;
            
            document.getElementById('transaction-results').innerHTML = '<div class="loading-spinner"></div> Searching...';
            
            fetch('/api/search-transactions', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({plate: plate, site: site})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('transaction-results').innerHTML = data.html;
            });
        }
    </script>
    {% endblock %}
    ''')

@app.route('/members')
@login_required
def members():
    return render_template_string(HTML_TEMPLATE + '''
    {% block content %}
    <div class="row">
        <div class="col-12">
            <h1 class="mb-4">Member Management</h1>
        </div>
    </div>
    
    <ul class="nav nav-tabs" role="tablist">
        <li class="nav-item">
            <a class="nav-link active" data-bs-toggle="tab" href="#members-tab">Members</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" data-bs-toggle="tab" href="#blacklist-tab">Blacklist</a>
        </li>
    </ul>
    
    <div class="tab-content">
        <!-- Members Tab -->
        <div id="members-tab" class="tab-pane active">
            <div class="dashboard-card">
                <h3>Add Member</h3>
                <div class="row">
                    <div class="col-md-8">
                        <input type="text" class="form-control" id="member-plate" 
                               placeholder="Enter license plate" style="text-transform: uppercase;">
                    </div>
                    <div class="col-md-4">
                        <button class="btn btn-custom w-100" onclick="addMember()">
                            <i class="fas fa-plus"></i> Add Member
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="dashboard-card mt-4">
                <h3>Current Members ({{ members|length }})</h3>
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>License Plate</th>
                                <th>Added</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for member in members %}
                            <tr>
                                <td><strong>{{ member }}</strong></td>
                                <td>{{ current_time }}</td>
                                <td>
                                    <button class="btn btn-sm btn-danger" 
                                            onclick="removeMember('{{ member }}')">
                                        <i class="fas fa-trash"></i> Remove
                                    </button>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- Blacklist Tab -->
        <div id="blacklist-tab" class="tab-pane">
            <div class="dashboard-card">
                <h3>Add to Blacklist</h3>
                <div class="row">
                    <div class="col-md-4">
                        <input type="text" class="form-control" id="blacklist-plate" 
                               placeholder="License plate" style="text-transform: uppercase;">
                    </div>
                    <div class="col-md-4">
                        <input type="text" class="form-control" id="blacklist-reason" 
                               placeholder="Reason">
                    </div>
                    <div class="col-md-4">
                        <button class="btn btn-danger w-100" onclick="addBlacklist()">
                            <i class="fas fa-ban"></i> Add to Blacklist
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="dashboard-card mt-4">
                <h3>Blacklisted Vehicles ({{ blacklist|length }})</h3>
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>License Plate</th>
                                <th>Reason</th>
                                <th>Added</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in blacklist %}
                            <tr>
                                <td><strong>{{ item['plate'] }}</strong></td>
                                <td>{{ item.get('reason', 'N/A') }}</td>
                                <td>{{ current_time }}</td>
                                <td>
                                    <button class="btn btn-sm btn-success" 
                                            onclick="removeBlacklist('{{ item['plate'] }}')">
                                        <i class="fas fa-check"></i> Remove
                                    </button>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    ''', members=member_plates, blacklist=[{'plate': p} for p in blacklist_plates], 
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M'))

@app.route('/visitor')
@login_required
def visitor():
    return render_template_string(HTML_TEMPLATE + '''
    {% block content %}
    <div class="row">
        <div class="col-12">
            <h1 class="mb-4">Create Visitor Pass</h1>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="dashboard-card">
                <h3>Visitor Information</h3>
                <form onsubmit="createVisitorPass(); return false;">
                    <div class="mb-3">
                        <label>License Plate</label>
                        <input type="text" class="form-control" id="visitor-plate" 
                               placeholder="Enter plate number" required style="text-transform: uppercase;">
                    </div>
                    <div class="mb-3">
                        <label>Valid for (hours)</label>
                        <select class="form-control" id="visitor-hours">
                            <option value="1">1 Hour</option>
                            <option value="2">2 Hours</option>
                            <option value="4" selected>4 Hours</option>
                            <option value="8">8 Hours</option>
                            <option value="24">24 Hours</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label>Site</label>
                        <select class="form-control" id="visitor-site">
                            <option value="4005">555 Capitol Mall</option>
                            <option value="4007">Bank of America</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-custom w-100">
                        <i class="fas fa-ticket-alt"></i> Create Pass
                    </button>
                </form>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="dashboard-card">
                <h3>Pass Details</h3>
                <div id="visitor-result">
                    <div class="text-center text-muted">
                        <i class="fas fa-ticket-alt fa-4x mb-3"></i>
                        <p>Fill in the form to create a visitor pass</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    ''')

@app.route('/cameras')
@login_required
def cameras():
    return render_template_string(HTML_TEMPLATE + '''
    {% block content %}
    <div class="row">
        <div class="col-12">
            <h1 class="mb-4">Camera Feeds</h1>
        </div>
    </div>
    
    <div class="alert alert-info">
        <i class="fas fa-info-circle"></i> Camera feeds update automatically every 5 seconds
    </div>
    
    <div class="row" id="camera-grid">
        <!-- Cameras will be loaded here -->
    </div>
    
    <script>
        function loadCameras() {
            fetch('/api/camera-feeds')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('camera-grid').innerHTML = data.html;
                });
        }
        
        loadCameras();
        setInterval(loadCameras, 5000);
    </script>
    {% endblock %}
    ''')

# API Routes
@app.route('/api/open-gate', methods=['POST'])
@login_required
def api_open_gate():
    data = request.json
    lane_id = data.get('lane_id')
    gate_name = data.get('gate_name')
    site_id = data.get('site_id', SITE_ID)
    
    url = f"{BASE_URL}/api/specialist/site/{site_id}/lane/{lane_id}/open-gate"
    headers = {
        "Authorization": f"Bearer {AUTH_KEY}",
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, timeout=10)
        if response.status_code in [200, 201, 204]:
            return jsonify({'success': True, 'message': f'{gate_name} opened successfully'})
        else:
            return jsonify({'success': False, 'message': f'Failed with status {response.status_code}'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/occupancy/<site_id>')
@login_required
def api_occupancy(site_id):
    url = f"{BASE_URL}/api/site/{site_id}/occupancy"
    headers = {"Authorization": f"Bearer {AUTH_KEY}", "Accept": "*/*"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            occupancy = data.get('currentOccupancy', 0)
            return jsonify({'html': str(occupancy)})
    except:
        pass
    return jsonify({'html': '--'})

@app.route('/api/waiting-count')
@login_required
def api_waiting_count():
    total = 0
    for site_id in ["4005", "4007"]:
        url = f"{BASE_URL}/api/specialist/site/{site_id}/event/hanging-exit/count"
        headers = {"Authorization": f"Bearer {AUTH_KEY}", "Accept": "*/*"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                total += data.get('count', 0)
        except:
            pass
    return jsonify({'html': str(total)})

@app.route('/api/recent-transactions')
@login_required  
def api_recent_transactions():
    html = '<div class="table-responsive"><table class="table table-sm">'
    html += '<thead><tr><th>Time</th><th>Plate</th><th>Site</th></tr></thead><tbody>'
    
    for site_id in ["4005", "4007"]:
        site_name = "555" if site_id == "4005" else "BoA"
        url = f"{BASE_URL}/api/specialist/site/{site_id}/visits/closed?count=5"
        headers = {"Authorization": f"Bearer {AUTH_KEY}", "Accept": "*/*"}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    transactions = data.get('data', {}).get('transactions', [])
                    for t in transactions[:5]:
                        vehicle = t.get('vehicle', {})
                        plate = vehicle.get('licensePlate', {}).get('text', 'Unknown') if vehicle else 'Unknown'
                        entry_time = t.get('entryTimestamp', '')
                        if entry_time:
                            entry_time = entry_time.split('T')[1][:5]
                        html += f'<tr><td>{entry_time}</td><td><strong>{plate}</strong></td><td>{site_name}</td></tr>'
        except:
            pass
    
    html += '</tbody></table></div>'
    return jsonify({'html': html})

@app.route('/api/members/add', methods=['POST'])
@login_required
def api_add_member():
    plate = request.json.get('plate', '').upper()
    if plate and plate not in member_plates:
        member_plates.append(plate)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Plate already exists or invalid'})

@app.route('/api/members/remove', methods=['POST'])
@login_required
def api_remove_member():
    plate = request.json.get('plate', '').upper()
    if plate in member_plates:
        member_plates.remove(plate)
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/api/blacklist/add', methods=['POST'])
@login_required
def api_add_blacklist():
    plate = request.json.get('plate', '').upper()
    if plate and plate not in blacklist_plates:
        blacklist_plates.append(plate)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Plate already blacklisted or invalid'})

@app.route('/api/blacklist/remove', methods=['POST'])
@login_required
def api_remove_blacklist():
    plate = request.json.get('plate', '').upper()
    if plate in blacklist_plates:
        blacklist_plates.remove(plate)
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/api/visitor-pass', methods=['POST'])
@login_required
def api_visitor_pass():
    data = request.json
    plate = data.get('plate', '').upper()
    hours = int(data.get('hours', 4))
    site_id = data.get('site_id', '4005')
    
    valid_until = datetime.now() + timedelta(hours=hours)
    site_name = "555 Capitol Mall" if site_id == "4005" else "Bank of America"
    
    # In a real app, you would save this to a database
    return jsonify({
        'success': True,
        'plate': plate,
        'valid_until': valid_until.strftime('%Y-%m-%d %H:%M'),
        'site': site_name
    })

@app.route('/api/camera-feeds')
@login_required
def api_camera_feeds():
    html = ''
    cameras = {
        '4005': [
            {'name': 'Entry Lane 1', 'lane': '17491'},
            {'name': 'Entry Lane 2', 'lane': '17492'},
            {'name': 'Exit Lane 3', 'lane': '17493'},
            {'name': 'Exit Lane 4', 'lane': '17494'},
        ],
        '4007': [
            {'name': 'Entry Lane 1', 'lane': '21173'},
            {'name': 'Entry Lane 2', 'lane': '21174'},
            {'name': 'Exit Lane 3', 'lane': '21175'},
            {'name': 'Exit Lane 4', 'lane': '21176'},
        ]
    }
    
    for site_id, cams in cameras.items():
        site_name = "555 Capitol Mall" if site_id == "4005" else "Bank of America"
        for cam in cams:
            html += f'''
            <div class="col-md-3 mb-4">
                <div class="camera-feed">
                    <h5>{site_name}</h5>
                    <h6>{cam['name']}</h6>
                    <div style="height: 200px; background: #333; display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-video fa-3x text-muted"></i>
                    </div>
                    <small class="text-muted">Lane {cam['lane']}</small>
                </div>
            </div>
            '''
    
    return jsonify({'html': html})

@app.route('/api/search-transactions', methods=['POST'])
@login_required
def api_search_transactions():
    data = request.json
    plate = data.get('plate', '').upper()
    site = data.get('site', 'all')
    
    html = '<div class="table-responsive"><table class="table">'
    html += '<thead><tr><th>Time</th><th>Plate</th><th>Duration</th><th>Site</th><th>Amount</th></tr></thead><tbody>'
    
    sites = ['4005', '4007'] if site == 'all' else [site]
    
    for site_id in sites:
        site_name = "555 Capitol" if site_id == "4005" else "Bank of America"
        url = f"{BASE_URL}/api/specialist/site/{site_id}/visits/closed?count=50"
        headers = {"Authorization": f"Bearer {AUTH_KEY}", "Accept": "*/*"}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    transactions = data.get('data', {}).get('transactions', [])
                    for t in transactions:
                        vehicle = t.get('vehicle', {})
                        t_plate = vehicle.get('licensePlate', {}).get('text', '') if vehicle else ''
                        
                        if plate and plate not in t_plate.upper():
                            continue
                        
                        entry_time = t.get('entryTimestamp', '')
                        exit_time = t.get('exitTimestamp', '')
                        amount = t.get('paymentDue', 0)
                        
                        if entry_time:
                            entry_time = entry_time.replace('T', ' ')[:16]
                        
                        duration = 'N/A'
                        if entry_time and exit_time:
                            try:
                                entry_dt = datetime.fromisoformat(t.get('entryTimestamp', '').replace('Z', '+00:00'))
                                exit_dt = datetime.fromisoformat(t.get('exitTimestamp', '').replace('Z', '+00:00'))
                                duration_td = exit_dt - entry_dt
                                hours = duration_td.seconds // 3600
                                minutes = (duration_td.seconds % 3600) // 60
                                duration = f'{hours}h {minutes}m'
                            except:
                                pass
                        
                        html += f'''
                        <tr>
                            <td>{entry_time}</td>
                            <td><strong>{t_plate}</strong></td>
                            <td>{duration}</td>
                            <td>{site_name}</td>
                            <td>${amount:.2f}</td>
                        </tr>
                        '''
        except Exception as e:
            print(f"Error searching transactions: {e}")
    
    html += '</tbody></table></div>'
    return jsonify({'html': html})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
