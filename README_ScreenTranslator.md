# Real-time Screen Translator

This program monitors a specific area of your screen, extracts text using Tesseract OCR, translates it using Google Translate, and displays the result in a real-time overlay.

## Requirements

1. Install system dependencies:
   - On Ubuntu/Debian: `sudo apt-get install tesseract-ocr python3-tk`
   - On Windows: Download and install Tesseract OCR from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki), and add the installation path to your system's PATH.
   - On macOS: `brew install tesseract tcl-tk`

2. Install Python dependencies:
   ```bash
   pip install mss pytesseract deep-translator Pillow
   ```

## Usage

1. Run the script:
   ```bash
   python screen_translator.py
   ```

2. Configure the area to capture:
   - **X**: Horizontal starting position (e.g., 0 for left edge).
   - **Y**: Vertical starting position (e.g., 800 for the bottom area on a 1080p screen).
   - **Width**: The width of the capture box.
   - **Height**: The height of the capture box.

3. Set Languages:
   - **Source Language**: Language of the game (e.g., `en` for English, `ja` for Japanese, or `auto` to auto-detect).
   - **Target Language**: Language to translate to (e.g., `pt` for Portuguese).

4. Click **Start Translation**.
   - An overlay window will appear.
   - It will automatically capture the configured screen area every second, read the text, translate it, and update the overlay.
   - You can drag the overlay window by clicking and holding on it.

## Limitations

- The OCR depends on the text contrast and font. Complex backgrounds or stylized fonts might not be recognized perfectly.
- To use languages other than English, make sure to install the respective Tesseract language data (e.g., `tesseract-ocr-jpn` for Japanese).
