import hashlib
import os
import json

HASH_FILE = 'file_hashes.json'

def calculate_file_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def scan_directory(directory):
    file_hashes = {}
    for root, dirs, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            hash_value = calculate_file_hash(path)
            if hash_value:
                file_hashes[path] = hash_value
    return file_hashes

def save_hashes(file_hashes):
    with open(HASH_FILE, 'w') as f:
        json.dump(file_hashes, f, indent=4)

def load_hashes():
    try:
        with open(HASH_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def compare_hashes(old_hashes, new_hashes):
    modified = []
    deleted = []
    new_files = []

    for path, old_hash in old_hashes.items():
        new_hash = new_hashes.get(path)
        if new_hash is None:
            deleted.append(path)
        elif new_hash != old_hash:
            modified.append(path)

    for path in new_hashes:
        if path not in old_hashes:
            new_files.append(path)

    return modified, deleted, new_files

def main():
    directory = input("Enter directory to scan: ")
    new_hashes = scan_directory(directory)
    old_hashes = load_hashes()

    if not old_hashes:
        print("No baseline hashes found. Saving current hashes.")
        save_hashes(new_hashes)
    else:
        modified, deleted, new_files = compare_hashes(old_hashes, new_hashes)

        if not (modified or deleted or new_files):
            print("No changes detected.")
        else:
            if modified:
                print("\nModified files:")
                for f in modified:
                    print(f)

            if deleted:
                print("\nDeleted files:")
                for f in deleted:
                    print(f)

            if new_files:
                print("\nNew files:")
                for f in new_files:
                    print(f)

        # Optional: update hash file after checking
        save_hashes(new_hashes)

if __name__ == "__main__":
    main()
