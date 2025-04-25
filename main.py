from src import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", # activate like this so your phone can access it.
        debug=True
    )