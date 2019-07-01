# Source: https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
import sys
import hashlib

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


def hash_from_file(file):
    sha1 = hashlib.sha1()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


if __name__ == '__main__':
    import os
    path = r"D:\01_Projects\18_animationProjects\projects\02_sagenkoenige\artwork\creatureA"
    content = os.listdir(path)
    for file in content:
        filepath = os.path.join(path, file)
        hash = hash_from_file(filepath)
        print(filepath)
        print(hash)
        print('++++++++++++++++')