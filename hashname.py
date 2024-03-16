# compute hash of the file and rename it to hash

import hashlib
import os
import argparse
import colorama


is_quiet = False
delete_dupes = False


def hash_sha256(file):
    sha256_hash = hashlib.sha256()
    with open(file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return 'sha256_' + sha256_hash.hexdigest()


def hash_md5(file):
    md5_hash = hashlib.md5()
    with open(file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return 'md5_' + md5_hash.hexdigest()


def hash_sha1(file):
    sha1_hash = hashlib.sha1()
    with open(file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha1_hash.update(byte_block)
    return 'sha1_' + sha1_hash.hexdigest()


def rename_file(file, new_name):
    global delete_dupes
    # get file extension
    extension = os.path.splitext(file)[1]
    new_name = new_name + extension
    base, ext = os.path.splitext(new_name)
    # rename file
    if delete_dupes \
            and os.path.exists(os.path.join(os.path.dirname(file), new_name)):
        os.remove(file)
        if not is_quiet:
            print('[INFO] File '
                  + colorama.Fore.LIGHTRED_EX + '"' + file + '"'
                  + colorama.Fore.RESET
                  + ' deleted'
                  )
    else:
        count = 0
        while os.path.exists(os.path.join(os.path.dirname(file), new_name)):
            count += 1
            new_name = base + "_" + str(count) + ext

        os.rename(file, os.path.join(os.path.dirname(file), new_name))
        if not is_quiet:
            print('[INFO] File '
                  + colorama.Fore.LIGHTRED_EX + '"' + file + '"'
                  + colorama.Fore.RESET
                  + ' -> '
                  + colorama.Fore.LIGHTGREEN_EX + '"' + new_name + '"'
                  + colorama.Fore.RESET)


def main():
    parser = argparse.ArgumentParser(
        description='Compute hash of the file and rename it to hash')
    parser.add_argument('-f', metavar='--filepath',
                        type=str, help='file to be hashed')
    parser.add_argument('-F', metavar='--folder', type=str,
                        help='folder with files to be hashed')
    parser.add_argument('-a', metavar='--algorithm',
                        type=str, help='hash algorithm')
    parser.add_argument('-q', metavar='--quiet', type=str, help='quiet mode')
    # recursive mode, flag
    parser.add_argument('-r', action='store_true', help='recursive mode')
    parser.add_argument('-D', action='store_true',
                        help='delete duplicate files')
    parser.add_argument('--force', action='store_true',
                        help='force recalculate hash')
    args = parser.parse_args()

    if args.D:
        global delete_dupes
        delete_dupes = args.D

    if args.a is None:
        args.a = 'sha256'

    if args.f:
        if args.a == 'sha256':
            rename_file(args.f, hash_sha256(args.f))
        elif args.a == 'md5':
            rename_file(args.f, hash_md5(args.f))
        elif args.a == 'sha1':
            rename_file(args.f, hash_sha1(args.f))
        else:
            if not is_quiet:
                print('Wrong algorithm')
        if not is_quiet:
            print('[INFO] File '
                  + colorama.Fore.LIGHTRED_EX + '"' + args.f + '"'
                  + colorama.Fore.RESET
                  + ' hashed'
                  )
    elif args.F:
        if args.r:
            for root, dirs, files in os.walk(args.F):
                for file in files:
                    if args.a == 'sha256':
                        if 'sha256_' in file and not args.force:
                            continue
                        rename_file(os.path.join(root, file),
                                    hash_sha256(os.path.join(root, file)))
                    elif args.a == 'md5':
                        if 'md5_' in file and not args.force:
                            continue
                        rename_file(os.path.join(root, file),
                                    hash_md5(os.path.join(root, file)))
                    elif args.a == 'sha1':
                        if 'sha1_' in file and not args.force:
                            continue
                        rename_file(os.path.join(root, file),
                                    hash_sha1(os.path.join(root, file)))
                    else:
                        if not is_quiet:
                            print('Wrong algorithm')
        else:
            for file in os.listdir(args.F):
                if os.path.isdir(os.path.join(args.F, file)):
                    continue
                if args.a == 'sha256':
                    if 'sha256_' in file and not args.force:
                        continue
                    rename_file(os.path.join(args.F, file),
                                hash_sha256(os.path.join(args.F, file)))
                elif args.a == 'md5':
                    if 'md5_' in file and not args.force:
                        continue
                    rename_file(os.path.join(args.F, file),
                                hash_md5(os.path.join(args.F, file)))
                elif args.a == 'sha1':
                    if 'sha1_' in file and not args.force:
                        continue
                    rename_file(os.path.join(args.F, file),
                                hash_sha1(os.path.join(args.F, file)))
                else:
                    if not is_quiet:
                        print('Wrong algorithm')
        if not is_quiet:
            print('[INFO] All files in folder '
                  + colorama.Fore.CYAN + '"' + args.F + '"'
                  + colorama.Fore.RESET + ' hashed'
                  )
    else:
        if not is_quiet:
            print('Wrong arguments')


if __name__ == '__main__':
    main()
