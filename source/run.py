from app import create_app
import webbrowser

app = create_app()

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True) 