python3 src/main.py "/"
echo "Starting server..."
cd docs && python3 -m http.server 8888
