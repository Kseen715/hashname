# hashname
<p align="center">
  <img src="https://github.com/Kseen715/imgs/blob/main/sakura_kharune.png?raw=true" width="160" height="160"/>
</p>

## Description
Simple renaming tool for files. It computes the hash of the file and renames it to the hash. Process is not reversible.

<p align="center">
  <img src="https://github.com/Kseen715/imgs/blob/main/hashname/hashname_anim.gif?raw=true"/>
</p>

## Usage

```
pyhton3 hashname.py -f [filepath]
```

Rename all files in a directory:

```
pyhton3 hashname.py -F [folder]
```

Rename all files in a directory recursively:

```
pyhton3 hashname.py -rF [folder]
```

Also, you can use the `-a` option to specify the algorithm to use. By default, it uses `sha256`. There are other options like `sha1` and `md5`.