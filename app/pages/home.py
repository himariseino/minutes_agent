import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        html.H1("Template Home Page"),
        html.P(
            "This is a template for creating a multi-page Dash app with Bootstrap components. "
            "This page is the home page."
        ),
        html.Div(
            [
                dcc.Link(
                    dbc.Button("Template Page", color="primary"),
                    href="/template",
                )
            ]
        ),
    ]
)
