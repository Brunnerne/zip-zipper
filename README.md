# zip-zipper
Tool for zipping, and then zipping again

By default all files are zipped into a single layer, but you can specify multiple layers, and each layer can have multiple files/folders.  
By default, all layers are encrypted with the same random password.

## Usage:

```
usage: Zip Zipper [-h] [-o OUTPUT_FILENAME] [-c COMPRESSION_LEVEL] [-n NUM_LAYERS] [-l LAYER [LAYER ...]] [--no_password] [-p PASSWORD] [-m]
                  [-so SAVE_PASSWORDS_FILE] [-sl SAVE_PASSWORDS_LAYER]
                  filenames [filenames ...]

Zips files/folders into a layered zip file

positional arguments:
  filenames             Files and folders to zip in layer 0

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                        Output filename
  -c COMPRESSION_LEVEL, --compression_level COMPRESSION_LEVEL
                        Compression level (1-9) (fastest - best compression)
  -n NUM_LAYERS, --num_layers NUM_LAYERS
                        Number of layers
  -l LAYER [LAYER ...], --layer LAYER [LAYER ...]
                        Files and folders to zip in each layer. Format: layernum:file1,file2 layernum2:file3,file4. Example: 1:file1,folder1 4:file2,file3
  --no_password         Do not use any passwords
  -p PASSWORD, --password PASSWORD
                        Password for the zip files, or outermost layer if -m is used
  -m, --multi_password  Use a different password for each layer
  -so SAVE_PASSWORDS_FILE, --save_passwords_file SAVE_PASSWORDS_FILE
                        Save passwords to a file, specify filename
  -sl SAVE_PASSWORDS_LAYER, --save_passwords_layer SAVE_PASSWORDS_LAYER
                        Save passwords to a layer, specify layer number
```