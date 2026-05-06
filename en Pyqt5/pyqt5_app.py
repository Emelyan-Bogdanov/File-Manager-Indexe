"""
PyQt5 File Indexer Application
Complete file indexing and search system.
"""

import sys
import json
import os
import random
import string
import platform
import subprocess
from pathlib import Path
from typing import List, Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QMessageBox,
    QScrollArea, QFrame, QDialog, QComboBox, QListWidget, QListWidgetItem,
    QProgressBar
)
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap, QBrush, QRegExpValidator
from PyQt5.QtCore import QRegExp

from pyqt5_styles import get_style_config, Theme, Colors
from pyqt5_search_service import SearchEngine, SearchResult


class FileIndexerApp(QMainWindow):
    """Main application window."""

    def __init__(self):
        """Initialize application."""
        super().__init__()
        
        self.style_config = get_style_config(Theme.LIGHT)
        self.search_engine = SearchEngine()
        
        # Set window properties
        self.setWindowTitle("File Indexer Pro")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Apply styles
        self.setStyleSheet(self.style_config.get_stylesheet())
        
        # Show splash screen
        self.show_splash_view()

    def show_splash_view(self):
        """Show splash screen."""
        widget = SplashView(self.style_config, self)
        self.setCentralWidget(widget)

    def show_add_view(self):
        """Show add files view."""
        widget = AddFileView(self.style_config, self)
        self.setCentralWidget(widget)

    def show_search_view(self):
        """Show search view."""
        widget = SearchView(self.style_config, self.search_engine, self)
        self.setCentralWidget(widget)


class SplashView(QWidget):
    """Splash screen with two main action buttons."""

    def __init__(self, style_config, parent):
        """Initialize splash view."""
        super().__init__()
        self.style_config = style_config
        self.parent = parent
        
        self.init_ui()

    def init_ui(self):
        """Build UI."""
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(40, 80, 40, 40)
        
        # Title
        title = QLabel("File Indexer Pro")
        title_font = QFont("Segoe UI", 32, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Organize, Find, and Manage Your Files Effortlessly")
        subtitle_font = QFont("Segoe UI", 12)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet(f"color: {self.style_config.get_color('text_secondary')};")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Divider
        divider = QFrame()
        divider.setStyleSheet(f"background-color: {self.style_config.get_color('border')}; height: 1px;")
        divider.setMaximumHeight(1)
        layout.addSpacing(20)
        layout.addWidget(divider)
        layout.addSpacing(20)
        
        # Buttons container
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        # Add Files button
        add_btn = self._create_action_button(
            "📁  Add Files",
            "Upload and organize\nnew files",
            self.parent.show_add_view
        )
        buttons_layout.addWidget(add_btn, 1)
        
        # Search Files button
        search_btn = self._create_action_button(
            "🔍  Search Files",
            "Find and retrieve\nyour files",
            self.parent.show_search_view
        )
        buttons_layout.addWidget(search_btn, 1)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        # Footer
        footer = QLabel("Keyboard shortcuts: Ctrl+A for Add Files • Ctrl+F for Search Files")
        footer_font = QFont("Segoe UI", 9)
        footer.setFont(footer_font)
        footer.setStyleSheet(f"color: {self.style_config.get_color('text_primary')};")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
        self.setLayout(layout)

    def _create_action_button(self, title: str, description: str, callback) -> QFrame:
        """Create an action button."""
        button_frame = QFrame()
        button_frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {self.style_config.get_color('bg_secondary')};
                border: 1px solid {self.style_config.get_color('border')};
                border-radius: 8px;
            }}
            QFrame:hover {{
                background-color: {self.style_config.get_color('primary')};
                border: 2px solid {self.style_config.get_color('primary')};
            }}
            """
        )
        button_frame.setMinimumHeight(200)
        button_frame.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel(title)
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_font = QFont("Segoe UI", 10)
        desc_label.setFont(desc_font)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet(f"color: {self.style_config.get_color('text_secondary')};")
        layout.addWidget(desc_label)
        
        button_frame.setLayout(layout)
        button_frame.mousePressEvent = lambda e: callback()
        
        return button_frame


class AddFileView(QWidget):
    """View for adding files and creating indexers."""

    def __init__(self, style_config, parent):
        """Initialize add file view."""
        super().__init__()
        self.style_config = style_config
        self.parent = parent
        self.selected_file = None
        
        self.init_ui()

    def init_ui(self):
        """Build UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(20)
        
        # Back button
        back_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setMaximumWidth(80)
        back_btn.clicked.connect(self.parent.show_splash_view)
        back_layout.addWidget(back_btn)
        back_layout.addStretch()
        layout.addLayout(back_layout)
        
        # Title
        title = QLabel("📁 Add New File")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # File selection section
        file_label = QLabel("Select File:")
        file_label_font = QFont("Segoe UI", 11, QFont.Bold)
        file_label.setFont(file_label_font)
        layout.addWidget(file_label)
        
        file_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        file_layout.addWidget(self.file_path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setMaximumWidth(100)
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        # Indexer form section
        form_label = QLabel("Indexer Information:")
        form_label_font = QFont("Segoe UI", 11, QFont.Bold)
        form_label.setFont(form_label_font)
        layout.addWidget(form_label)
        
        # Filename
        layout.addWidget(QLabel("Custom File Name:"))
        self.filename_edit = QLineEdit()
        self.filename_edit.setPlaceholderText("Enter custom name for this file")
        layout.addWidget(self.filename_edit)
        
        # Description
        layout.addWidget(QLabel("Description:"))
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Enter description/notes for this file")
        self.description_edit.setMaximumHeight(80)
        layout.addWidget(self.description_edit)
        
        # Keywords/Tags
        layout.addWidget(QLabel("Tags/Keywords:"))
        tags_layout = QHBoxLayout()
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Enter tags separated by commas (e.g., work, important)")
        tags_layout.addWidget(self.tags_edit)
        layout.addLayout(tags_layout)
        
        layout.addSpacing(10)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        reset_btn = QPushButton("Reset")
        reset_btn.setMaximumWidth(100)
        reset_btn.clicked.connect(self.reset_form)
        button_layout.addWidget(reset_btn)
        
        submit_btn = QPushButton("Submit")
        submit_btn.setMaximumWidth(100)
        submit_btn.clicked.connect(self.submit_form)
        button_layout.addWidget(submit_btn)
        
        layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def browse_file(self):
        """Open file browser."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "All Files (*.*)"
        )
        if file_path:
            self.selected_file = file_path
            self.file_path_edit.setText(file_path)

    def reset_form(self):
        """Reset form fields."""
        self.filename_edit.clear()
        self.description_edit.clear()
        self.tags_edit.clear()
        self.selected_file = None
        self.file_path_edit.clear()

    def submit_form(self):
        """Submit and create indexer."""
        # Validation
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a file")
            return
        
        if not os.path.exists(self.selected_file):
            QMessageBox.warning(self, "Error", "Selected file no longer exists")
            return
        
        filename = self.filename_edit.text().strip()
        description = self.description_edit.toPlainText().strip()
        tags_text = self.tags_edit.text().strip()
        
        if not filename or not description or not tags_text:
            QMessageBox.warning(self, "Error", "All fields are required")
            return
        
        # Parse tags
        keywords = [tag.strip() for tag in tags_text.split(",") if tag.strip()]
        
        # Create indexer JSON
        indexer_data = {
            "filename": filename,
            "filepath": self.selected_file,
            "description": description,
            "keywords": keywords
        }
        
        # Create indexers folder if not exists
        indexers_folder = Path("indexers")
        indexers_folder.mkdir(exist_ok=True)
        
        # Generate random filename
        random_name = "indexer_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ".json"
        indexer_path = indexers_folder / random_name
        
        # Save indexer
        try:
            with open(indexer_path, "w", encoding="utf-8") as f:
                json.dump(indexer_data, f, indent=2)
            
            QMessageBox.information(self, "Success", "Indexer created successfully!")
            self.reset_form()
            self.parent.search_engine._load_all_indexers()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create indexer: {e}")


class SearchView(QWidget):
    """View for searching indexed files."""

    def __init__(self, style_config, search_engine, parent):
        """Initialize search view."""
        super().__init__()
        self.style_config = style_config
        self.search_engine = search_engine
        self.parent = parent
        self.current_results: List[SearchResult] = []
        
        self.init_ui()

    def init_ui(self):
        """Build UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)
        
        # Back button
        back_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setMaximumWidth(80)
        back_btn.clicked.connect(self.parent.show_splash_view)
        back_layout.addWidget(back_btn)
        back_layout.addStretch()
        layout.addLayout(back_layout)
        
        # Title
        title = QLabel("🔍 Search Files")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Search input
        layout.addWidget(QLabel("Enter search terms (separated by spaces):"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by filename, tags, or description...")
        self.search_input.textChanged.connect(self.on_search_input)
        layout.addWidget(self.search_input)
        
        # Results count
        self.results_count_label = QLabel("Results: 0")
        self.results_count_label.setStyleSheet(f"color: {self.style_config.get_color('text_secondary')};")
        layout.addWidget(self.results_count_label)
        
        # Results area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(
            f"QScrollArea {{ background-color: {self.style_config.get_color('bg_primary')}; border: none; }}"
        )
        
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_layout.setSpacing(10)
        self.results_container.setLayout(self.results_layout)
        
        scroll_area.setWidget(self.results_container)
        layout.addWidget(scroll_area)
        
        # No results label
        self.no_results_label = QLabel("Start typing to search for files...")
        self.no_results_label.setStyleSheet(f"color: {self.style_config.get_color('text_primary')};")
        self.no_results_label.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(self.no_results_label)
        
        self.setLayout(layout)

    def on_search_input(self, text: str):
        """Handle search input changes."""
        query = text.strip()
        
        # Clear results
        while self.results_layout.count() > 1:
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not query:
            self.no_results_label.show()
            self.results_count_label.setText("Results: 0")
            return
        
        # Search
        results = self.search_engine.search(query)
        self.current_results = results
        
        if not results:
            self.no_results_label.setText("No results found.")
            self.no_results_label.show()
            self.results_count_label.setText("Results: 0")
            return
        
        self.no_results_label.hide()
        self.results_count_label.setText(f"Results: {len(results)}")
        
        # Create search words for highlighting
        search_words = self.search_engine._normalize_text(query)
        
        # Display results
        for result in results:
            result_card = self._create_result_card(result, search_words)
            self.results_layout.insertWidget(self.results_layout.count() - 1, result_card)

    def _create_result_card(self, result: SearchResult, search_words: List[str]) -> QFrame:
        """Create a result card widget."""
        card = QFrame()
        
        # Set border color based on file existence
        if result.file_exists:
            card.setStyleSheet(
                f"""
                QFrame {{
                    background-color: {self.style_config.get_color('bg_secondary')};
                    border: 1px solid {self.style_config.get_color('border')};
                    border-radius: 6px;
                }}
                QFrame:hover {{
                    border: 2px solid {self.style_config.get_color('primary')};
                }}
                """
            )
        else:
            card.setStyleSheet(
                f"""
                QFrame {{
                    background-color: {self.style_config.get_color('bg_secondary')};
                    border: 2px solid {self.style_config.get_color('error')};
                    border-radius: 6px;
                }}
                """
            )
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(8)
        
        # Top: Filename + Buttons
        top_layout = QHBoxLayout()
        
        filename_label = QLabel(result.filename)
        filename_font = QFont("Segoe UI", 12, QFont.Bold)
        filename_label.setFont(filename_font)
        top_layout.addWidget(filename_label)
        
        top_layout.addStretch()
        
        # Open button
        open_btn = QPushButton("Open")
        open_btn.setMaximumWidth(80)
        open_btn.clicked.connect(lambda: self._open_file(result))
        open_btn.setEnabled(result.file_exists)
        top_layout.addWidget(open_btn)
        
        # Open in Explorer button
        explorer_btn = QPushButton("Open in Explorer")
        explorer_btn.setMaximumWidth(120)
        explorer_btn.clicked.connect(lambda: self._open_in_explorer(result))
        explorer_btn.setEnabled(result.file_exists)
        top_layout.addWidget(explorer_btn)
        
        layout.addLayout(top_layout)
        
        # File path
        path_label = QLabel(result.filepath)
        path_label.setStyleSheet(
            f"color: {self.style_config.get_color('text_primary')}; font-size: 9pt;"
        )
        layout.addWidget(path_label)
        
        # Description
        if result.description:
            desc_label = QLabel(result.description)
            desc_label.setStyleSheet(f"color: {self.style_config.get_color('text_primary')};")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Tags
        if result.keywords:
            tags_layout = QHBoxLayout()
            tags_layout.addWidget(QLabel("Tags:"))
            
            for keyword in result.keywords:
                is_match = keyword.lower() in search_words
                tag_label = QLabel(f"#{keyword}")
                
                if is_match:
                    tag_label.setStyleSheet(
                        f"""
                        QLabel {{
                            background-color: {self.style_config.get_color('primary')};
                            color: white;
                            padding: 4px 8px;
                            border-radius: 4px;
                        }}
                        """
                    )
                else:
                    tag_label.setStyleSheet(
                        f"""
                        QLabel {{
                            background-color: {self.style_config.get_color('bg_tertiary')};
                            color: {self.style_config.get_color('text_secondary')};
                            padding: 4px 8px;
                            border-radius: 4px;
                        }}
                        """
                    )
                
                tags_layout.addWidget(tag_label)
            
            tags_layout.addStretch()
            layout.addLayout(tags_layout)
        
        card.setLayout(layout)
        return card

    def _open_file(self, result: SearchResult):
        """Open file."""
        if not os.path.exists(result.filepath):
            QMessageBox.warning(self, "Error", "File not found or has been moved.")
            return
        
        try:
            if platform.system() == "Windows":
                os.startfile(result.filepath)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", result.filepath])
            else:
                subprocess.Popen(["xdg-open", result.filepath])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {e}")

    def _open_in_explorer(self, result: SearchResult):
        """Open folder in explorer."""
        if not os.path.exists(result.filepath):
            QMessageBox.warning(self, "Error", "File not found or has been moved.")
            return
        
        try:
            folder_path = os.path.dirname(result.filepath)
            
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer /select,"{result.filepath}"')
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-R", result.filepath])
            else:
                subprocess.Popen(["nautilus", folder_path])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open folder: {e}")


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    window = FileIndexerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
