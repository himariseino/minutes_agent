import dash_bootstrap_components as dbc


def create_navbar():
    """Create navbar component.

    Returns
    -------
        dbc.NavbarSimple: Navbar component

    """
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Template", href="/template")),
        ],
        brand="Template",
        brand_href="/",
        color="#212A37",
        dark=True,
    )
    return navbar
