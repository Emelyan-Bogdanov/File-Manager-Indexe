# File Indexer Pro - PyQt5 Application

A professional file indexing and search application built with PyQt5. Organize and find your files easily by adding custom metadata (tags, descriptions) and searching through them intelligently.

## Features

### 🎯 Core Features
- **Add Files**: Create indexers for files with custom names, descriptions, and tags
- **Smart Search**: Search by filename, keywords, or description with word-based matching
- **File Validation**: Detects missing or moved files automatically
- **Quick Access**: Open files directly or reveal them in file explorer
- **Relevance Ranking**: Results sorted by match relevance

### 💡 Smart Search Algorithm
- Case-insensitive word matching
- Multi-field search (filename, keywords, description)
- Relevance scoring:
  - Filename matches: 30% weight
  - Keyword matches: 10% weight
  - Description matches: Base weight
- Maximum 50 results per search

### 🎨 User Interface
- Clean, modern design with light theme
- Responsive layouts
- Professional color scheme
- Keyboard shortcuts (Ctrl+A, Ctrl+F)
- Real-time search feedback

## Project Structure

```
pyqt5_file_indexer/
├── pyqt5_app.py                 # Main application
├── pyqt5_search_service.py      # Search engine logic
├── pyqt5_styles.py              # Theme and styling
├── pyqt5_requirements.txt        # Dependencies
├── indexers/                     # Indexer JSON files (auto-created)
└── README.md
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone/Download the project**
```bash
cd pyqt5_file_indexer
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r pyqt5_requirements.txt
```

## Usage

### Running the Application

```bash
python pyqt5_app.py
```

### Main Views

#### 1. Splash Screen
The welcome screen with two main actions:
- **Add Files**: Create a new file indexer
- **Search Files**: Search existing indexers

#### 2. Add File View
Create an indexer for a file:
1. Click "Browse..." to select a file
2. Enter custom file name
3. Add description/notes
4. Add tags (comma-separated, e.g., "work, important, project")
5. Click "Submit" to create the indexer

Example:
```
File: Document.pdf
Custom Name: Q3 Financial Report
Description: Quarterly financial review and analysis
Tags: finance, q3, important, work
```

#### 3. Search View
Find your indexed files:
1. Type search terms (space-separated)
2. Results appear in real-time
3. Click "Open" to open the file
4. Click "Open in Explorer" to view folder

Example searches:
- `finance` → finds indexers with "finance" in any field
- `work important` → finds indexers with both words
- `project` → finds indexers with "project" in filename, tags, or description

## Indexer JSON Format

Each indexer is a JSON file in the `indexers/` folder:

```json
{
  "filename": "Q3 Financial Report",
  "filepath": "C:\\Users\\Documents\\finance_q3.pdf",
  "description": "Quarterly financial review and analysis",
  "keywords": [
    "finance",
    "q3",
    "important",
    "work"
  ]
}
```

## Search Algorithm Details

### Step 1: Word Normalization
Input: `"Work IMPORTANT project"`
Output: `["work", "important", "project"]`
- Converts to lowercase
- Removes punctuation
- Splits into words

### Step 2: Multi-Field Search
For each indexer, search:
1. **Filename** (custom name)
2. **Keywords** (tags array)
3. **Description** (full text)

### Step 3: Relevance Scoring
```
Score = (matched_words / total_search_words) * 0.5
       + (has_filename_match ? 0.3 : 0)
       + (has_keyword_match ? 0.1 : 0)
       + (has_description_match ? 0.1 : 0)
```

Example:
- Query: "work project"
- Indexer has "work" in filename and "project" in keywords
- Score: (2/2)*0.5 + 0.3 + 0.1 + 0 = 0.9 (90% relevant)

### Step 4: Result Display
- Results sorted by score (highest first)
- Maximum 50 results displayed
- Keywords matching search are highlighted

## File Status Indicators

### ✅ File Exists
- Normal styling
- "Open" and "Open in Explorer" buttons enabled
- Clickable card

### ❌ File Missing/Moved
- Red border on result card
- "Open" and "Open in Explorer" buttons disabled
- Tooltip: "⚠ This file doesn't exist"
- Card is still visible for reference

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+A | Go to Add Files view |
| Ctrl+F | Go to Search view |
| Enter | Submit form (Add view) |
| Escape | Back to splash screen |

## File Operations

### Open File
Opens the file with the default application for its type:
- PDF → PDF reader
- DOC/DOCX → Word processor
- MP3 → Media player
- etc.

### Open in Explorer
Reveals the file's folder in file explorer:
- **Windows**: Selects file in Explorer
- **macOS**: Shows file in Finder
- **Linux**: Opens folder in Nautilus

## Advanced Features

### File Existence Checking
- Automatically verifies file paths
- Handles moved/deleted files gracefully
- No error crashes

### Relevance-Based Ranking
Smart sorting ensures most relevant results appear first

### Persistent Storage
- Indexers saved as JSON files
- Portable across computers
- Easy to backup

### Cross-Platform Support
- Works on Windows, macOS, Linux
- File operations adapted per OS
- Path handling compatible with all systems

## Styling

The application uses a modern light theme with:
- **Primary Color**: Blue (#1e40af)
- **Secondary Color**: Purple (#7c3aed)
- **Error Color**: Red (#dc2626)
- **Background**: White (#ffffff)
- **Text**: Dark gray (#111827)

To switch themes, modify:
```python
self.style_config = get_style_config(Theme.LIGHT)  # or Theme.DARK
```

## Troubleshooting

### Issue: "No module named PyQt5"
**Solution**: Install PyQt5
```bash
pip install PyQt5
```

### Issue: File not opening
**Solution**: Ensure file exists and hasn't been moved. Check file permissions.

### Issue: Search returns no results
**Solution**: Ensure you've added indexers (Add Files view). Check search terms.

### Issue: "This file doesn't exist"
**Solution**: The indexed file has been moved or deleted. Either:
- Move/restore the file to original location
- Create a new indexer for the current file location

## Performance Tips

- Keep descriptions concise (100-200 characters ideal)
- Use meaningful tags (avoid generic terms)
- Limit tags to 3-5 per file
- Perform searches on relevant keywords

## Future Enhancements

Potential additions:
- Export/Import indexers
- Batch file operations
- Advanced filtering
- Full-text search
- Dark theme
- Custom themes
- Cloud sync
- Duplicate detection

## License

Open source - feel free to modify and distribute

## Support

For issues or suggestions, check the code comments or create an issue.

## Technical Details

### Architecture
- **MVC Pattern**: Models (SearchEngine), Views (PyQt5), Controllers (App)
- **Separation of Concerns**: Search logic separate from UI
- **Scalable Design**: Easy to add new views

### Dependencies
- **PyQt5**: GUI framework
- **Standard Library**: json, os, pathlib, re, subprocess

### File Size
- ~800 lines of code
- Minimal dependencies
- Fast startup time

## Author

Created as a professional file management solution.

---

**Version**: 1.0  
**Last Updated**: 2026  
**Python**: 3.8+
