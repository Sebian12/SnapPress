# Photo Compressor

A desktop application for compressing JPEG and PNG photos without visible quality loss. Built with Python and customtkinter.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Pillow](https://img.shields.io/badge/Pillow-10.x-green) ![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)

## Features

- Drag & drop support
- Batch compression (multiple files at once)
- Adjustable quality slider (1–95%)
- Progress bar with live feedback
- Savings summary (before / after / % saved)
- Saves compressed files next to originals — originals are never overwritten

## Screenshots

![Empty](assets/empty.png)
![After compression](assets/one_file_comp.png)
![Multiple files](assets/multiple_files_comp.png)

## Requirements

- Python 3.10+
- Pillow

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sebian12/photo-compressor.git
cd photo-compressor
```

2. Install dependencies:
```bash
pip install Pillow
```

3. Run the app:
```bash
python main.py
```

## Usage

1. Drag and drop photos into the window, or click **Choose photos**
2. Adjust the quality slider (default: 80%)
3. Click **Compress and save**
4. Compressed files are saved in the same folder as the originals with a `_compressed` suffix

## Roadmap

- [ ] Android port
- [ ] EXIF metadata preservation
- [ ] Custom output folder
- [x] Dark mode

## Tech stack

- Python 3.14
- customtkinter — GUI
- Pillow — image processing

## License

MIT
