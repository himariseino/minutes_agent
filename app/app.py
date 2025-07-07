import os
import warnings

import dash
import dash_bootstrap_components as dbc
from components.footer import create_footer
from components.navbar import create_navbar
from dash import Dash, html

warnings.filterwarnings("ignore")

# Initialize the app
app = Dash(
    __name__,
    assets_folder=os.path.join(os.path.dirname(__file__), "assets"),
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,  # Enable pages
)

app.title = "Template"

# Create the app layout
app.layout = html.Div(
    [
        create_navbar(),
        dash.page_container,
        create_footer(),
    ],
    className="app-container",
)


def main():
    """Run the app."""
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
