from flask import Flask, request, render_template_string, abort
from key import authenticate

app = Flask(__name__)
# Dictionary to store rankings
rankings = {}

# HTML template for leaderboard page
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="10">
    <title>Leaderboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: white;
            color: black;
        }
        .leaderboard-container {
            text-align: center;
        }
        h1 {
            font-size: 2em;
            margin-bottom: 20px;
        }
        .leaderboard {
            margin-top: 20px;
            font-size: 1.5em;
        }
        .leaderboard-item {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="leaderboard-container">
        <img src="{{url_for('static', filename='logo.png')}}" width="100" height="100"/>
        <h1>Leaderboard</h1>
        <div class="leaderboard">
            {% for name, points in rankings %}
                <div class="leaderboard-item">{{ loop.index }}. {{ name }}: {{ points }}</div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

def get_sorted_rankings():
    """Sort rankings based on points in descending order and return top 10."""
    return sorted(rankings.items(), key=lambda x: x[1], reverse=True)[:10]

@app.route('/')
def leaderboard():
    """Render the leaderboard page."""
    sorted_rankings = get_sorted_rankings()
    return render_template_string(html_template, rankings=sorted_rankings)

@app.route('/s')
def submit_score():
    """Endpoint to receive name, points, and key to update leaderboard."""
    # Retrieve parameters
    name = request.args.get('n')
    points = request.args.get('p', type=int)
    key = request.args.get('k')

    # Validate the key
    if not authenticate(key):
        abort(403)  # Return a 403 Forbidden if the key is incorrect

    # Validate name and points
    if not name or points is None:
        abort(400)  # Return a 400 Bad Request if parameters are missing

    # Update the rankings
    rankings[name] = points

    return "Score submitted successfully!", 200

if __name__ == '__main__':
    app.run(debug=True)
