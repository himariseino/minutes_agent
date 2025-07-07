import dash
from dash import html

dash.register_page(__name__, path="/template")

layout = html.Div(
    [
        html.H1("Template Page"),
        html.P(
            "This is a template for creating a multi-page Dash app with Bootstrap components. "
            "This page is the template page."
        ),
    ]
)
