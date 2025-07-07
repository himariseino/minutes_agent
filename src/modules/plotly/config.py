from pathlib import Path
from typing import Annotated, ClassVar, Literal

import plotly.graph_objects as go
import plotly.io as pio
from plotly.graph_objs.layout import Legend
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

HexColor = Annotated[str, Field(pattern=r"^#[0-9a-fA-F]{6}$")]
ColorValue = Annotated[str, Field(pattern=r"^#[0-9a-fA-F]{6}$|^[a-zA-Z]+$")]


class ColorScheme(BaseModel):
    """Color scheme configuration.

    Attributes
    ----------
        background: Background color
        base: Base color for primary elements
        primary: Primary color for emphasis
        secondary: Secondary color for complementary elements
        success: Color for success states
        info: Color for informational states
        warning: Color for warning states
        danger: Color for error states
        light: Light color for subtle elements
        dark: Dark color for strong contrast
        text: Text color
        grid: Grid line color
        primary_light: Lighter variant of primary color
        secondary_light: Lighter variant of secondary color
        base_light: Lighter variant of base color
        train_line: Color for training data lines
        valid_line: Color for validation data lines
        train_marker: Color for training data markers
        perfect_line: Color for perfect prediction line
        table_header: Color for table headers
        table_cell: Color for table cells

    """

    model_config = ConfigDict(frozen=True)

    # Base colors
    background: HexColor = "#FCFCFC"
    base: HexColor = "#003366"
    primary: HexColor = "#F56B60"
    secondary: HexColor = "#20B2AA"
    success: HexColor = "#28A745"
    info: HexColor = "#17A2B8"
    warning: HexColor = "#FFC107"
    danger: HexColor = "#DC3545"
    light: HexColor = "#F8F9FA"
    dark: HexColor = "#343A40"
    text: HexColor = "#2F2F2F"
    grid: HexColor = "#E5E5E5"

    # Extended colors
    primary_light: HexColor = "#F78B83"
    secondary_light: HexColor = "#40D2CA"
    base_light: HexColor = "#204D80"

    # Plot specific colors
    train_line: ColorValue = "royalblue"
    valid_line: ColorValue = "coral"
    train_marker: ColorValue = "royalblue"
    perfect_line: ColorValue = "red"
    table_header: ColorValue = "royalblue"
    table_cell: ColorValue = "lavender"

    @model_validator(mode="after")
    def validate_color_contrast(self) -> "ColorScheme":
        """Validate that text color has sufficient contrast with background color."""
        # This is a placeholder for potential color contrast validation
        # You could implement actual color contrast checking here
        return self


class LineStyle(BaseModel):
    """Line style configuration for plots."""

    model_config = ConfigDict(frozen=True)

    color: str = Field(..., description="Line color")
    width: int = Field(2, ge=1, le=10, description="Line width in pixels")
    dash: Literal["solid", "dash", "dot", "dashdot"] = Field("solid", description="Line dash style")


class MarkerStyle(BaseModel):
    """Marker style configuration for plots."""

    model_config = ConfigDict(frozen=True)

    size: int = Field(8, ge=1, le=20, description="Marker size in pixels")
    opacity: float = Field(0.7, ge=0.0, le=1.0, description="Marker opacity (0.0 to 1.0)")


class TraceStyle(BaseModel):
    """Style configuration for a single trace."""

    model_config = ConfigDict(frozen=True)

    line: LineStyle = Field(..., description="Line style configuration")


class PlotDefaults(BaseModel):
    """Default plot style configurations.

    Attributes
    ----------
        train_style: Style for training data traces
        valid_style: Style for validation data traces
        marker_style: Style for markers/points
        perfect_line_style: Style for perfect prediction line

    """

    model_config = ConfigDict(frozen=True)

    train_style: TraceStyle = Field(..., description="Training data trace style")
    valid_style: TraceStyle = Field(..., description="Validation data trace style")
    marker_style: MarkerStyle = Field(..., description="Marker style configuration")
    perfect_line_style: TraceStyle = Field(..., description="Perfect prediction line style")

    @classmethod
    def create_defaults(cls, colors: ColorScheme) -> "PlotDefaults":
        """Create default plot styles using provided color scheme.

        Args:
        ----
            colors: Color scheme configuration

        Returns:
        -------
            PlotDefaults: Default plot style configurations

        """
        return cls(
            train_style=TraceStyle(line=LineStyle(color=colors.train_line, width=2, dash="solid")),
            valid_style=TraceStyle(line=LineStyle(color=colors.valid_line, width=2, dash="solid")),
            marker_style=MarkerStyle(size=8, opacity=0.7),
            perfect_line_style=TraceStyle(line=LineStyle(color=colors.perfect_line, width=2, dash="dash")),
        )


class LayoutConfig(BaseModel):
    """Layout configuration.

    Attributes
    ----------
        font_family: Font family for all text elements
        title_font_size: Font size for titles
        axis_font_size: Font size for axis labels
        legend_font_size: Font size for legend text

    """

    model_config = ConfigDict(frozen=True)

    font_family: str = Field("Arial, sans-serif", pattern=r"^[a-zA-Z\s,-]+$")
    title_font_size: int = Field(ge=1, le=72, default=24)
    axis_font_size: int = Field(ge=1, le=72, default=14)
    legend_font_size: int = Field(ge=1, le=72, default=10)

    @field_validator("font_family")
    @classmethod
    def validate_font_family(cls, v: str) -> str:
        """Validate font family string."""
        valid_fonts = {"Arial", "Helvetica", "sans-serif", "serif"}
        fonts = {f.strip() for f in v.split(",")}
        if not any(font in valid_fonts for font in fonts):
            raise ValueError("Font family must include at least one standard web-safe font")
        return v


class PlotlyConfig:
    """Configuration for Plotly."""

    # Class variables
    path_to_save_figure: ClassVar[Path] = Path("../outputs/deck/static")
    colors: ClassVar[ColorScheme] = ColorScheme()
    layout: ClassVar[LayoutConfig] = LayoutConfig()

    def __init__(self):
        """Initialize the Plotly configuration."""
        self._init_legend()
        self._init_plot_defaults()
        self._init_layout_defaults()

    def _init_legend(self) -> None:
        """Initialize legend configuration."""
        self.legend: Legend = Legend(
            bgcolor=self.colors.background,
            bordercolor=self.colors.grid,
            borderwidth=1,
            font=dict(
                family=self.layout.font_family,
                size=self.layout.axis_font_size,
                color=self.colors.text,
            ),
            orientation="h",
            itemsizing="constant",
            itemwidth=30,
            itemclick="toggle",
            itemdoubleclick="toggleothers",
            traceorder="normal",
            tracegroupgap=10,
            y=1.01,
            yanchor="bottom",
            x=0.01,
            xanchor="left",
            title=dict(
                text=None,
                font=dict(
                    family=self.layout.font_family,
                    size=self.layout.axis_font_size,
                    color=self.colors.base,
                ),
            ),
        )

    def _init_plot_defaults(self) -> None:
        """Initialize plot default styles."""
        self.plot_defaults: PlotDefaults = PlotDefaults(
            train_style=TraceStyle(line=LineStyle(color=self.colors.train_line, width=2, dash="solid")),
            valid_style=TraceStyle(line=LineStyle(color=self.colors.valid_line, width=2, dash="solid")),
            marker_style=MarkerStyle(size=8, opacity=0.7),
            perfect_line_style=TraceStyle(line=LineStyle(color=self.colors.perfect_line, width=2, dash="dash")),
        )

    def _init_layout_defaults(self) -> None:
        """Initialize layout default styles."""
        self.layout_defaults = {
            "plot_bgcolor": self.colors.background,
            "paper_bgcolor": self.colors.background,
            "font": {"color": self.colors.text, "family": self.layout.font_family},
            "xaxis": {
                "gridcolor": self.colors.grid,
                "linecolor": self.colors.dark,
                "titlefont": {"color": self.colors.base},
                "tickfont": {"color": self.colors.text},
            },
            "yaxis": {
                "gridcolor": self.colors.grid,
                "linecolor": self.colors.dark,
                "titlefont": {"color": self.colors.base},
                "tickfont": {"color": self.colors.text},
            },
        }

    @classmethod
    def set_custom_plotly_template(cls) -> None:
        """Set custom template for Plotly.

        Returns
        -------
            None

        Docs:
            https://plotly.com/python/templates/

        """
        pio.templates["custom_template"] = go.layout.Template(
            layout=go.Layout(
                paper_bgcolor=cls.colors.background,
                plot_bgcolor=cls.colors.background,
            )
        )
        pio.templates.default = "custom_template"

    @classmethod
    def save_png(cls, fig: go.Figure, filename: str, width: int = 1200, height: int = 500) -> None:
        """Save the given Plotly figure as a PNG file.

        Args:
        ----
            fig: The Plotly figure to save
            filename: The name of the file to save the figure as
            width: The width of the saved image. Defaults to 1200
            height: The height of the saved image. Defaults to 500

        Returns:
        -------
            None

        """
        fig.write_image(cls.path_to_save_figure / f"{filename}.png", width=width, height=height)
