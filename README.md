# Photo Compressor

A desktop application for compressing JPEG and PNG photos without visible quality loss. Built with Python and customtkinter.

![Python](https://img.shields.io/badge/Python-3.14-blue) ![Pillow](https://img.shields.io/badge/Pillow-12.x-green) ![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)

## Features

- Drag & drop support (not yet)
- Batch compression (multiple files at once)
- Adjustable quality slider (1–95%)
- Progress bar with live feedback
- Savings summary (before / after)
- Saves compressed files next to originals — originals are never overwritten

## Screenshots

![Empty](assets/empty.png)
![Dark mode](assets/dark_mode.png)
![After compression](assets/one_file_comp.png)
![Multiple files](assets/multiple_files_comp.png)

## Requirements

- Python 3.10+
- Pillow

## Installation

### Universal (Windows, macOS, Linux)
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

### Windows only

1. Download .exe file from current release

## Usage

1. Drag and drop photos into the window, or click **Choose photos**
2. Adjust the quality slider (default: 80%)
3. Click **Compress and save**
4. Compressed files are saved in the same folder as the originals with a `_compressed` suffix or saved in selected folder

## Roadmap

- [x] Dark mode (1.2.0)
- [x] Settings menu (1.3.0)
- [x] Custom output folder (1.4.0)
- [x] Settings saver (1.5.0)
- [x] File counter (1.5.0)
- [x] Button to clear photo list or single photo (1.5.0)
- [ ] Compressed file size next to file name (1.6.0)
- [ ] Thumbnails of photos (1.7.0)
- [ ] Optimization (1.8.0)
- [ ] EXIF metadata preservation (1.9.0)
- [ ] Drag & Drop support (1.10.0)
- [ ] Android port (2.0.0)

## Tech stack

- Python 3.14
- customtkinter — GUI
- Pillow — image processing

## License

MIT
