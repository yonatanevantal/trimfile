import os
from pathlib import Path
from tempfile import gettempdir
from argparse import ArgumentParser


DEFAULT_OUTPUT_FILE_NAME = "trimmed_file"
DEFAULT_OUTPUT_FILE_PATH = Path(gettempdir()) / DEFAULT_OUTPUT_FILE_NAME


class TrimOptions:
    END = "end"    
    START = "start"


def create_parser():
    _parser = ArgumentParser(description="Remove given number of bytes from "
                                         "the start or end of a file.")
    _parser.add_argument("input_file", type=Path, action="store", 
                         help="Full path to the file to trim.")
    _parser.add_argument("bytes", type=int, action="store", 
                         help="Number of bytes to trim.")
    _parser.add_argument("side", choices=["start", "end"], 
                         help="Whether to trim from the start.")
    _parser.add_argument("-d", "--destination-file", type=str, action="store", 
                         default=DEFAULT_OUTPUT_FILE_PATH)
    return _parser


def get_bytes_to_read(path, bytes):
    return os.path.getsize(path) - bytes


def main():
    args = create_parser().parse_args()
    bytes_to_read = get_bytes_to_read(args.input_file, args.bytes)
    
    with open(args.input_file, 'rb') as infile:
        if args.side == TrimOptions.START:
            data = infile.read()[bytes_to_read:]
        elif args.side == TrimOptions.END:
            data = infile.read()[:bytes_to_read]
    
    with open(args.destination_file, "wb") as outfile:
        outfile.write(data)
        

if __name__ == '__main__':
    main()
