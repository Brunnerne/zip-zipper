# zip-zipper
Tool for zipping, and then zipping again

By default all files are zipped into a single layer, but you can specify multiple layers, and each layer can have multiple files/folders.  
By default, all layers are encrypted with the same random password.

## Usage:

```
usage: Zip Zipper [-h] [-p PASSWORD] [--no_password] [-l LAYER [LAYER ...]] [-o OUTPUT_FILENAME] [-n NUM_LAYERS] [-c COMPRESSION_LEVEL] [-m]
                  filenames [filenames ...]

Zips files/folders into a layered zip file

positional arguments:
  filenames             Files and folders to zip in layer 0

options:
  -h, --help            show this help message and exit
  -p PASSWORD, --password PASSWORD
                        Password for the zip files, or outermost layer if -m is used
  --no_password         Do not use any passwords
  -l LAYER [LAYER ...], --layer LAYER [LAYER ...]
                        Files and folders to zip in each layer. Format: layernum:file1,file2 layernum2:file3,file4. Example: 1:file1,folder1
                        4:file2,file3
  -o OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                        Output filename
  -n NUM_LAYERS, --num_layers NUM_LAYERS
                        Number of layers
  -c COMPRESSION_LEVEL, --compression_level COMPRESSION_LEVEL
                        Compression level (1-9) (fastest - best compression)
  -m, --multi_password  Use a different password for each layer
```