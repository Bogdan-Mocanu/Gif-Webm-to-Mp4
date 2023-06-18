
import os
import shlex
import ffmpy


def get_files_with_subfolders(src_folder, extensions):
    source_files = []
    for root, dirs, files in os.walk(src_folder):
        for name in files:
            if name.endswith(extensions):
                source_files.append(os.path.join(root, name))
    return source_files


def get_files(src_folder, extensions):
    source_files = []
    for item in os.listdir(src_folder):
        if os.path.isfile(os.path.join(src_folder, item)) and item.endswith(extensions):
            source_files.append(os.path.join(src_folder, item))
    return source_files


def convert_gif(input_path, output_path):
    ff = ffmpy.FFmpeg(
        inputs={input_path: None},
        outputs={output_path: '-movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"'}
    )
    try:
        ff.run()
    except ffmpy.FFRuntimeError:
        print("Could not convert " + file)


def convert_webm(input_path, output_path):
    ff = ffmpy.FFmpeg(
        inputs={input_path: None},
        outputs={output_path: '-c:v libx264'}
    )
    try:
        ff.run()
    except ffmpy.FFRuntimeError:
        print("Could not convert " + file)


def validate_input(input_string):

    options = ('s', 'f', 'm')
    input_split = shlex.split(input_string)

    src_path = input_split[0]
    dst_path = input_split[1]
    option = input_split[2]

    # Checks if source_folder is empty
    if not os.path.isfile(src_path):
        if not os.path.isdir(src_path) or not os.listdir(src_path):
            print(f"{src_path} does not exist or is empty")
            return

    # Checks if destination folder exists and creates folder structure if not
    if not os.path.isdir(dst_path):
        answer = input(f"{dst_path} does not exist, do you wish to create it? y/n")
        if answer == "y" or answer == "Y":
            os.makedirs(dst_path)
        elif answer == "n" or answer == "N":
            return
        else:
            print("Invalid answer.")
            return

    if option not in options:
        return

    return input_split


def create_subfolders(file_path):
    # Create the directory structure for the file if it doesn't exist
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)


def get_file_folder(file):
    split_char = '\\'
    k = file.count('\\')
    temp = file.split('\\')
    folder = split_char.join(temp[:k])
    return folder


def convert_file(file, dst_path):
    # Keep file name / folder structure after conversion
    src_path = get_file_folder(file)
    rel_path = os.path.relpath(file, src_path)
    end_path = os.path.join(dst_path, rel_path)

    (base, ext) = os.path.splitext(end_path)

    file_dst = base + ".mp4"
    if file.endswith('.gif'):
        convert_gif(file, file_dst)
    elif file.endswith('.webm'):
        convert_webm(file, file_dst)


if __name__ == '__main__':

    extensions_list = (".gif", ".webm")

    while True:
        parameters = input('Input:')
        validated_parameters = validate_input(parameters)
        if validated_parameters:
            src_folder = validated_parameters[0]
            dst_folder = validated_parameters[1]
            argument = validated_parameters[2]
            match argument:
                case 's':
                    convert_file(src_folder, dst_folder)
                case 'f':
                    files = get_files(src_folder, extensions_list)
                    for file in files:
                        convert_file(file, dst_folder)
                case 'm':
                    files = get_files_with_subfolders(src_folder, extensions_list)
                    for file in files:
                        create_subfolders(file)
                        convert_file(file, dst_folder)
                case _:
                    print('invalid option')

