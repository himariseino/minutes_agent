from datetime import datetime

import dash_bootstrap_components as dbc
from dash import html


def create_footer() -> html.Div:
    """Create footer component.

    Returns
    -------
        html.Div: Footer component

    """
    current_year = datetime.now().year

    footer = html.Footer(
        dbc.Container(
            [
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            html.P(
                                ["Template ", html.Sup("©"), f" {current_year}"],
                                className="text-center text-muted",
                            ),
                            width=12,
                        )
                    ]
                ),
            ]
        ),
        className="footer mt-auto py-3",
    )

    return footer
