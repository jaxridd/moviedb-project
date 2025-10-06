#!/usr/bin/env python3
"""
Script to export local MySQL database for team sharing
Run this to export your local moviedb data
"""

import subprocess
import os
from datetime import datetime

def export_database():
    """Export local MySQL database to SQL file"""
    
    # Database connection details (update these for your local setup)
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',  # Update with your MySQL password
        'database': 'moviedb'
    }
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"moviedb_export_{timestamp}.sql"
    
    # Build mysqldump command
    cmd = [
        'mysqldump',
        f"--host={db_config['host']}",
        f"--user={db_config['user']}",
        f"--password={db_config['password']}",
        '--single-transaction',
        '--routines',
        '--triggers',
        db_config['database']
    ]
    
    try:
        print(f"Exporting database to {filename}...")
        
        # Run mysqldump
        with open(filename, 'w', encoding='utf-8') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"✅ Database exported successfully to {filename}")
            print(f"📁 File size: {os.path.getsize(filename)} bytes")
            print(f"\n📋 Next steps:")
            print(f"1. Share {filename} with your team")
            print(f"2. Import to Railway MySQL database")
            print(f"3. Update DATABASE_URL in Railway environment variables")
        else:
            print(f"❌ Export failed: {result.stderr}")
            
    except FileNotFoundError:
        print("❌ mysqldump not found. Make sure MySQL is installed and in PATH")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_import_instructions():
    """Show instructions for importing to Railway"""
    print("\n" + "="*50)
    print("📖 IMPORT INSTRUCTIONS FOR RAILWAY")
    print("="*50)
    print("""
1. Go to Railway dashboard → Your project
2. Add MySQL database service
3. Get connection details from Railway
4. Import using one of these methods:

Method A - Command line:
mysql -h [railway_host] -u [railway_user] -p [railway_db] < moviedb_export_YYYYMMDD_HHMMSS.sql

Method B - MySQL Workbench:
1. Create new connection to Railway database
2. Use Railway connection details
3. Import SQL file

5. Update Railway environment variable:
DATABASE_URL=mysql+pymysql://[user]:[password]@[host]:[port]/[database]
""")

if __name__ == "__main__":
    print("🗄️  Movie Database Export Tool")
    print("="*40)
    
    # Check if we can connect to local MySQL
    try:
        import pymysql
        connection = pymysql.connect(
            host='localhost',
            user='root', 
            password='root',  # Update this
            database='moviedb'
        )
        connection.close()
        print("✅ Local MySQL connection successful")
        export_database()
        show_import_instructions()
    except Exception as e:
        print(f"❌ Cannot connect to local MySQL: {e}")
        print("\n💡 Make sure:")
        print("- MySQL is running locally")
        print("- Database 'moviedb' exists")
        print("- Update password in this script")
        print("- Install pymysql: pip install pymysql")
