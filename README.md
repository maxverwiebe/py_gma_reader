# py_gma_reader

py_gma_reader is a Python library for reading and extracting Garry's Mod Addon (GMA) files. It provides an easy-to-use interface to access metadata and extract the contents of GMA files.

## Features

- Read metadata from GMA files, including:
  - Addon name
  - Author
  - Description
  - Addon type
  - Tags
  - Version
  - File list
- Extract the contents of a GMA file to a specified directory
- Concurrent file extraction for improved performance

## Installation

Clone this repo.

## Usage

Here's a simple example of how to use py_gma_reader:

```python
from py_gma_reader import AddonReader

file_path = "path/to/addon.gma"
with open(file_path, "rb") as file:
    reader = AddonReader(file)
    addon = reader.parse_addon()
    
    print(addon)  # Print addon metadata
    
    extraction_path = "path/to/extraction/directory"
    addon.extract_files(extraction_path)  # Extract addon files
```


## API

### `AddonReader`

The `AddonReader` class is the main entry point for reading GMA files. It takes a file-like object as input and provides methods to parse the addon metadata and extract the files.

#### Methods

- `parse_addon()`: Parses the GMA file and returns a `GModAddon` object containing the addon metadata and file list.

### `GModAddon`

The `GModAddon` class represents a Garry's Mod addon and provides access to its metadata and file list.

#### Attributes

- `name`: The name of the addon.
- `author`: The author of the addon.
- `description`: The description of the addon.
- `addon_type`: The type of the addon (e.g., gamemode, map, weapon).
- `tags`: A list of tags associated with the addon.
- `version`: The version of the addon.
- `files`: A list of `AddonFile` objects representing the files in the addon.

#### Methods

- `extract_files(destination)`: Extracts the files of the addon to the specified destination directory.

### `AddonFile`

The `AddonFile` class represents a file within a Garry's Mod addon.

#### Attributes

- `file_id`: The unique identifier of the file.
- `name`: The name of the file.
- `size`: The size of the file in bytes.
- `crc`: The CRC checksum of the file.
- `offset`: The offset of the file within the GMA file.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.