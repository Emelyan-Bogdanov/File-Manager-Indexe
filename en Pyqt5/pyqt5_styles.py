"""
PyQt5 Styles Module
Centralized style configuration with modern aesthetic.
"""

from enum import Enum


class Theme(Enum):
    """Available themes."""
    LIGHT = "light"
    DARK = "dark"


class Colors:
    """Color palette."""
    
    # Light theme
    PRIMARY_LIGHT = "#1e40af"
    SECONDARY_LIGHT = "#7c3aed"
    ACCENT_LIGHT = "#dc2626"
    
    BG_PRIMARY_LIGHT = "#ffffff"
    BG_SECONDARY_LIGHT = "#f9fafb"
    BG_TERTIARY_LIGHT = "#f3f4f6"
    
    TEXT_PRIMARY_LIGHT = "#111827"
    TEXT_SECONDARY_LIGHT = "#6b7280"
    TEXT_TERTIARY_LIGHT = "#9ca3af"
    
    BORDER_LIGHT = "#e5e7eb"
    SUCCESS_LIGHT = "#16a34a"
    WARNING_LIGHT = "#ea580c"
    ERROR_LIGHT = "#dc2626"
    
    # Dark theme
    PRIMARY_DARK = "#3b82f6"
    SECONDARY_DARK = "#a78bfa"
    ACCENT_DARK = "#ef4444"
    
    BG_PRIMARY_DARK = "#111827"
    BG_SECONDARY_DARK = "#1f2937"
    BG_TERTIARY_DARK = "#374151"
    
    TEXT_PRIMARY_DARK = "#f9fafb"
    TEXT_SECONDARY_DARK = "#d1d5db"
    TEXT_TERTIARY_DARK = "#9ca3af"
    
    BORDER_DARK = "#4b5563"
    SUCCESS_DARK = "#22c55e"
    WARNING_DARK = "#f97316"
    ERROR_DARK = "#ef4444"


class StyleConfig:
    """Style configuration manager."""

    def __init__(self, theme: Theme = Theme.LIGHT):
        """Initialize with theme."""
        self.current_theme = theme
        self._palette = self._build_palette()

    def _build_palette(self) -> dict:
        """Build color palette."""
        if self.current_theme == Theme.LIGHT:
            return {
                "primary": Colors.PRIMARY_LIGHT,
                "secondary": Colors.SECONDARY_LIGHT,
                "accent": Colors.ACCENT_LIGHT,
                "bg_primary": Colors.BG_PRIMARY_LIGHT,
                "bg_secondary": Colors.BG_SECONDARY_LIGHT,
                "bg_tertiary": Colors.BG_TERTIARY_LIGHT,
                "text_primary": Colors.TEXT_PRIMARY_LIGHT,
                "text_secondary": Colors.TEXT_SECONDARY_LIGHT,
                "text_tertiary": Colors.TEXT_TERTIARY_LIGHT,
                "border": Colors.BORDER_LIGHT,
                "success": Colors.SUCCESS_LIGHT,
                "warning": Colors.WARNING_LIGHT,
                "error": Colors.ERROR_LIGHT,
            }
        else:
            return {
                "primary": Colors.PRIMARY_DARK,
                "secondary": Colors.SECONDARY_DARK,
                "accent": Colors.ACCENT_DARK,
                "bg_primary": Colors.BG_PRIMARY_DARK,
                "bg_secondary": Colors.BG_SECONDARY_DARK,
                "bg_tertiary": Colors.BG_TERTIARY_DARK,
                "text_primary": Colors.TEXT_PRIMARY_DARK,
                "text_secondary": Colors.TEXT_SECONDARY_DARK,
                "text_tertiary": Colors.TEXT_TERTIARY_DARK,
                "border": Colors.BORDER_DARK,
                "success": Colors.SUCCESS_DARK,
                "warning": Colors.WARNING_DARK,
                "error": Colors.ERROR_DARK,
            }

    def get_color(self, color_name: str) -> str:
        """Get color from palette."""
        return self._palette.get(color_name, "#000000")

    def set_theme(self, theme: Theme) -> None:
        """Change theme."""
        self.current_theme = theme
        self._palette = self._build_palette()

    def get_stylesheet(self) -> str:
        """Get QSS stylesheet for entire application."""
        bg_primary = self.get_color("bg_primary")
        bg_secondary = self.get_color("bg_secondary")
        text_primary = self.get_color("text_primary")
        text_secondary = self.get_color("text_secondary")
        primary = self.get_color("primary")
        border = self.get_color("border")

        return f"""
            QMainWindow {{
                background-color: {bg_primary};
                color: {text_primary};
            }}
            
            QWidget {{
                background-color: {bg_primary};
                color: {text_primary};
            }}
            
            QPushButton {{
                background-color: {primary};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 10pt;
            }}
            
            QPushButton:hover {{
                background-color: {self.get_color("secondary")};
            }}
            
            QPushButton:pressed {{
                background-color: {primary};
                opacity: 0.8;
            }}
            
            QPushButton:disabled {{
                background-color: {text_primary};
                color: {text_secondary};
            }}
            
            QLineEdit {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 8px;
                font-size: 10pt;
            }}
            
            QLineEdit:focus {{
                border: 2px solid {primary};
            }}
            
            QTextEdit {{
                background-color: {bg_secondary};
                color: {text_primary};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 8px;
                font-size: 10pt;
            }}
            
            QTextEdit:focus {{
                border: 2px solid {primary};
            }}
            
            QScrollBar:vertical {{
                background-color: {bg_secondary};
                width: 12px;
                border: none;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {border};
                border-radius: 6px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {primary};
            }}
            
            QLabel {{
                color: {text_primary};
            }}
            
            QFrame {{
                background-color: {bg_primary};
                border: none;
            }}
        """


# Global style config instance
_style_config = None


def get_style_config(theme: Theme = Theme.LIGHT) -> StyleConfig:
    """Get or create global StyleConfig."""
    global _style_config
    if _style_config is None:
        _style_config = StyleConfig(theme)
    return _style_config
