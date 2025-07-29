#!/usr/bin/env python3
"""
Simple PostgreSQL Database Viewer
A web-based GUI to view your PostgreSQL database tables and data
"""
import os
from dotenv import load_dotenv
from flask import Flask, render_template_string, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    """Get database connection"""
    database_url = os.environ.get('DATABASE_URL')
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

@app.route('/')
def index():
    """Main database viewer page"""
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>PostgreSQL Database Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .tables-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .table-card { background: #007bff; color: white; padding: 15px; border-radius: 5px; cursor: pointer; text-align: center; transition: background 0.3s; }
        .table-card:hover { background: #0056b3; }
        .data-container { margin-top: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .info { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .error { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .loading { text-align: center; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐘 PostgreSQL Database Viewer</h1>
        <div class="info">
            <strong>Database:</strong> sacco_postgre<br>
            <strong>Host:</strong> dpg-d24gta3uibrs73bur5r0-a.oregon-postgres.render.com
        </div>
        
        <h2>📋 Tables</h2>
        <div class="tables-list" id="tables-list">
            <div class="loading">Loading tables...</div>
        </div>
        
        <div class="data-container" id="data-container"></div>
    </div>

    <script>
        // Load tables on page load
        window.onload = function() {
            loadTables();
        };

        function loadTables() {
            fetch('/api/tables')
                .then(response => response.json())
                .then(data => {
                    const tablesContainer = document.getElementById('tables-list');
                    if (data.error) {
                        tablesContainer.innerHTML = '<div class="error">Error: ' + data.error + '</div>';
                        return;
                    }
                    
                    tablesContainer.innerHTML = '';
                    data.tables.forEach(table => {
                        const tableCard = document.createElement('div');
                        tableCard.className = 'table-card';
                        tableCard.textContent = table;
                        tableCard.onclick = () => loadTableData(table);
                        tablesContainer.appendChild(tableCard);
                    });
                })
                .catch(error => {
                    document.getElementById('tables-list').innerHTML = '<div class="error">Error loading tables: ' + error + '</div>';
                });
        }

        function loadTableData(tableName) {
            const dataContainer = document.getElementById('data-container');
            dataContainer.innerHTML = '<div class="loading">Loading data for ' + tableName + '...</div>';
            
            fetch('/api/table/' + tableName)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        dataContainer.innerHTML = '<div class="error">Error: ' + data.error + '</div>';
                        return;
                    }
                    
                    let html = '<h2>📊 Table: ' + tableName + '</h2>';
                    html += '<div class="info">Rows: ' + data.rows.length + '</div>';
                    
                    if (data.rows.length > 0) {
                        html += '<table><thead><tr>';
                        Object.keys(data.rows[0]).forEach(column => {
                            html += '<th>' + column + '</th>';
                        });
                        html += '</tr></thead><tbody>';
                        
                        data.rows.forEach(row => {
                            html += '<tr>';
                            Object.values(row).forEach(value => {
                                html += '<td>' + (value !== null ? value : '<em>NULL</em>') + '</td>';
                            });
                            html += '</tr>';
                        });
                        html += '</tbody></table>';
                    } else {
                        html += '<div class="info">No data in this table.</div>';
                    }
                    
                    dataContainer.innerHTML = html;
                })
                .catch(error => {
                    dataContainer.innerHTML = '<div class="error">Error loading table data: ' + error + '</div>';
                });
        }
    </script>
</body>
</html>
    """)

@app.route('/api/tables')
def get_tables():
    """Get list of all tables"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = [row['table_name'] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({'tables': tables})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/table/<table_name>')
def get_table_data(table_name):
    """Get data from a specific table"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Sanitize table name (basic protection)
        if not table_name.replace('_', '').isalnum():
            return jsonify({'error': 'Invalid table name'})
        
        cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 100;')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({'rows': rows})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🚀 Starting PostgreSQL Database Viewer...")
    print("📍 Open your browser and go to: http://localhost:5001")
    print("🔗 Database: sacco_postgre")
    print("⚠️  Press Ctrl+C to stop the server")
    app.run(debug=True, port=5001)