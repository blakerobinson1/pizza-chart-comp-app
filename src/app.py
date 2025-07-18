from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Welcome to the Pizza Chart App!"),
    html.P("This is a landing page for your player comparison visualizations. More features coming soon!")
])

if __name__ == "__main__":
    app.run(debug=True)
