from traveltogetherapp import create_app
from flask_login import login_required
from flask import render_template

app = create_app()

# Main page route
@app.route('/main')
@login_required
def main_page():
    return render_template('main_page.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
