import pyminizip
import argparse
import os
import tempfile
import shutil
import secrets

parser = argparse.ArgumentParser(
                    prog='Zip Zipper',
                    description='Zips files/folders into a layered zip file')
parser.add_argument('filenames', nargs='+', help='Files and folders to zip in layer 0')
parser.add_argument('-p', '--password', help='Password for the zip files, or outermost layer if -m is used')
parser.add_argument('--no_password', action='store_true', help='Do not use any passwords')
parser.add_argument('-l', '--layer', nargs='+', help='Files and folders to zip in each layer. Format: layernum:file1,file2 layernum2:file3,file4. Example: 1:file1,folder1 4:file2,file3')
parser.add_argument('-o', '--output_filename', default='output.zip', help='Output filename')
parser.add_argument('-n', '--num_layers', type=int, default=1, help='Number of layers')
parser.add_argument('-c', '--compression_level', type=int, default=5, help='Compression level (1-9) (fastest - best compression)')
parser.add_argument('-m', '--multi_password', action='store_true', help='Use a different password for each layer')
parser.add_argument('-so', '--save_passwords_file', help='Save passwords to a file, specify filename')
parser.add_argument('-sl', '--save_passwords_layer', type=int, help='Save passwords to a layer, specify layer number')

args = parser.parse_args()

layers = [[] for i in range(args.num_layers)]

# Add filenames to layer 0
layers[0] = args.filenames

# Add filenames to other layers
if args.layer:
    for layer in args.layer:
        layer = layer.split(':')
        if len(layer) != 2:
            print('Invalid layer format')
            exit()
        layer_num = int(layer[0])
        if layer_num >= args.num_layers:
            print('Layer number must be less than the number of layers')
            exit()
        filenames = layer[1].split(',')
        layers[layer_num].extend(filenames)

# Make sure the save passwords layer is valid
if args.save_passwords_layer and args.save_passwords_layer >= args.num_layers:
    print('Layer number must be less than the number of layers')
    exit()

compression_level = args.compression_level

output_filename = args.output_filename or 'output.zip'
output_filename = output_filename if output_filename.endswith('.zip') else output_filename + '.zip'

# Check that filenames exists and are located in the current directory
# Get current dir
current_dir = os.getcwd()

for layer in layers:
    for filename in layer:
        # Get absolute path of filename
        filename = os.path.abspath(filename)
        # Check that filename is in current dir
        if not filename.startswith(current_dir):
            print('All files must be in the current directory')
            exit()

def get_zip_name():
    return 'zip' + secrets.token_hex(16) + '.zip'

def resolve_folder(folder):
    # Get all files in the folder and subfolders
    files = []
    paths = []
    for path, _, filenames in os.walk(folder):
        for filename in filenames:
            files.append(filename)
            paths.append(path)
    # Make filenames relative to the parent of the folder
    files = [os.path.join(paths[i], files[i]) for i in range(len(files))]

    return (files,paths)

def compress_multiple(files, paths, password, compression_level, temp_dir):
    zip_name = get_zip_name()
    # Compress the files
    pyminizip.compress_multiple(files, paths, os.path.join(temp_dir, zip_name), password, compression_level)

    return zip_name

def compress_layer(layer, password, compression_level, temp_dir):
    files = []
    paths = []

    for file in layer:
        if os.path.isfile(file):
            files.append(file)
            paths.append("")
        elif os.path.isdir(file):
            (f, p) = resolve_folder(file)
            files.extend(f)
            paths.extend(p)
        else:
            print('File does not exist: ' + file)
            exit()

    return compress_multiple(files, paths, password, compression_level, temp_dir)

def print_layers(layers):
    for i in range(len(layers)):
        print('Layer', i, ':', layers[i])

def print_passwords(passwords):
    for i in range(len(passwords)):
        print('Password', i, ':', passwords[i])

# Create a temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    # Create passwords for layers
    passwords = []
    if args.multi_password:
        for i in range(args.num_layers):
            passwords.append(secrets.token_hex(16))
        # Set the last password to the user specified password
        if args.password:
            passwords[-1] = args.password
    else:
        # Set all passwords to the user specified password or the same random password
        rand_pass = secrets.token_hex(16)
        passwords = [args.password or rand_pass for i in range(args.num_layers)]

    # Set all passwords to None if no_password is specified
    if args.no_password:
        passwords = [None for i in range(args.num_layers)]

    # Save passwords to a file
    if args.save_passwords_file or args.save_passwords_layer:
        with open(os.path.join(temp_dir, "passwords.txt"), 'w') as f:
            for i, password in enumerate(passwords):
                f.write('Password ' + str(i) + ': ' + str(password))
        if args.save_passwords_file:
            shutil.copy(os.path.join(temp_dir, "passwords.txt"), args.save_passwords_file)
        if args.save_passwords_layer:
            layers[int(args.save_passwords_layer)].append(os.path.join(temp_dir, "passwords.txt"))

    # Compress the first layer
    zip_name = compress_layer(layers[0], passwords[0], compression_level, temp_dir)
    
    # Compress the rest of the layers
    for i in range(1,args.num_layers):
        layers[i].append(os.path.join(temp_dir,zip_name))
        zip_name = compress_layer(layers[i], passwords[i], compression_level, temp_dir)

    # Move the final zip to the output filename
    shutil.move(os.path.join(temp_dir, zip_name), output_filename)

    # Print results
    print_passwords(passwords)
    print_layers(layers)