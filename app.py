from dash import Dash, dcc, html, Input, Output, State
import psycopg2
import os

# Read DB credentials from environment variables
DB_HOST     = os.environ.get("DB_HOST")
DB_PORT     = os.environ.get("DB_PORT", 5432)
DB_NAME     = os.environ.get("DB_NAME")
DB_USER     = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

def create_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS numbers (id SERIAL PRIMARY KEY, value INTEGER)"
    )
    conn.commit()
    cur.close()
    conn.close()

def insert_number(value):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO numbers (value) VALUES (%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()

def get_numbers():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT value FROM numbers ORDER BY id ASC")
    numbers = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return numbers

# Create the database table if needed
create_db()

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2("Enter a number:"),
    dcc.Input(id="num-input", type="number"),
    html.Button("Submit", id="submit-btn"),
    html.Div(id="result"),
    html.Hr(),
    html.H4("Previously entered numbers:"),
    html.Ul(id="numbers-list")
])

@app.callback(
    Output("result", "children"),
    Output("numbers-list", "children"),
    Input("submit-btn", "n_clicks"),
    State("num-input", "value"),
    prevent_initial_call=False  # So the list loads at startup
)
def handle_submission(n_clicks, value):
    msg = ""
    if n_clicks and value is not None:
        insert_number(value)
        msg = f"Stored {value}"
    numbers = get_numbers()
    nums_list = [html.Li(str(num)) for num in numbers]
    return msg, nums_list

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")