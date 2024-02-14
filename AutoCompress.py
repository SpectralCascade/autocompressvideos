import os
import ffmpeg
import argparse
import subprocess
import traceback

def compress_to_mp4(path, output_path, delete_original=False):
    try:
        fs = ffmpeg.input(path)
        fs = ffmpeg.output(fs, output_path)
        fs.run(overwrite_output=True)
        print(f"Compressed file \"{path}\" to \"{output_path}\"")
        if delete_original:
            os.remove(path)
    except subprocess.CalledProcessError as e:
        print(f"ERROR compressing file \"{path}\" during subprocess: {e}")
    except Exception as e:
        print(f"ERROR compressing file \"{path}\" (generic): {e}")

def compress_directory(path, delete_original=False):
    print(f"Compressing video files at path \"{path}\"...")
    
    path = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        print(f"Checking root {root}")
        for filename in files:
            if filename.lower().endswith(".mkv") or filename.lower().endswith(".avi"):
                base = os.path.splitext(filename)[0]
                output_path = os.path.join(path, base + ".mp4")
                compress_to_mp4(os.path.join(root, filename), output_path, delete_original)

def main():
    parser = argparse.ArgumentParser(description="Compress MKV and AVI files to MP4 in all sub-directories.")
    parser.add_argument("path", help="Directory path to recurse through with MKV and AVI files.")
    parser.add_argument("--delete", action="store_true", help="Delete original files after converting to MP4.")
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"ERROR: Path \"{args.path}\" does not exist.")
        return
    
    print("Compressing files...")
    compress_directory(args.path, args.delete)

if __name__ == "__main__":
    main()
