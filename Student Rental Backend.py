from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data representing rooms in the database
rooms = [
    {
        "room_id": 1,
        "location": "Downtown",
        "price": 500,
        "room_type": "single",
        "amenities": ["wifi", "parking"]
    },
    {
        "room_id": 2,
        "location": "Uptown",
        "price": 700,
        "room_type": "shared",
        "amenities": ["wifi", "ac"]
    },
    {
        "room_id": 3,
        "location": "Suburb",
        "price": 300,
        "room_type": "single",
        "amenities": ["parking"]
    }
]

@app.route('/search', methods=['GET'])
def search_rooms():
    # Get query parameters
    location = request.args.get('location', '').lower()
    price_range = request.args.get('price_range', '')
    room_type = request.args.get('room_type', '').lower()
    amenities = request.args.getlist('amenities')

    # Parse price range
    min_price, max_price = (0, float('inf'))
    if price_range:
        try:
            min_price, max_price = map(int, price_range.split('-'))
        except ValueError:
            return jsonify({"error": "Invalid price range format. Use min-max."}), 400

    # Filter rooms based on criteria
    filtered_rooms = []
    for room in rooms:
        if location and location not in room['location'].lower():
            continue
        if not (min_price <= room['price'] <= max_price):
            continue
        if room_type and room_type != room['room_type']:
            continue
        if amenities and not all(amenity in room['amenities'] for amenity in amenities):
            continue
        filtered_rooms.append(room)

    return jsonify(filtered_rooms)

if __name__ == '__main__':
    app.run(debug=True)
