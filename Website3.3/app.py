from webpage import create_app

# Create a Flask app
app = create_app()

if __name__=="__main__":
    app.run(debug=True)