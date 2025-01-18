from app import create_app  # Assuming you have a create_app function in __init__.py

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
