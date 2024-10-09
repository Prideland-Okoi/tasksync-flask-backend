from api import create_app, db
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Run the application using the Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)
