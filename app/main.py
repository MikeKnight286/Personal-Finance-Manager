from app import create_app  # Assuming your package is named app

app = create_app()

if __name__ == '__main__':
    # Running the Flask application
    app.run(debug=True)
