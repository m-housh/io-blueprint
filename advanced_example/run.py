from app import io, create_app

app = create_app(debug=True)

if __name__ == '__main__':
    io.run(app)
