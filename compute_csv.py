import os
import os.path
import argparse
import re
re_size = re.compile(r'(con|con.body|ind|var).xml')

db = {}

outfile = None

def log(*args):
    print(" ", *args)
    outfile.write("|".join((*args,)))
    outfile.write("\n")

def in_folder(path, *files):
    for f in files:
        if os.path.isfile(os.path.join(path, f)):
            return True
    return False

def getURI(path, *things):
    path = path[1:]
    uri = (path + os.path.join("/", *things)).rstrip("/")
    return "cic:" + (uri if uri else "/")

def walk(callback_file, callback_dir, root):
    callback_dir(root)
    files = os.listdir(root)
    for filename in files:
        j = os.path.join(root, filename)
        if os.path.isfile(j):
            callback_file(root, filename)
        elif os.path.isdir:
            walk(callback_file, callback_dir, j)

def processTheoryXML(path):
    with open(path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            one = re.search('<ht:DEFINITION uri="(.*)" as="(.*)" line="', line, re.IGNORECASE)
            if one:
                log("Definition", one.group(1))
                log("As", one.group(1), one.group(2))
            two = re.search('<ht:THEOREM uri="(.*)" as="(.*)" line="', line, re.IGNORECASE)
            if two:
                log("Theorem", two.group(1))
                log("As", two.group(1), two.group(2))

def f_dir(path):
    parent = os.path.abspath(os.path.join(path, os.pardir))
    A = os.path.basename(path)
    if not in_folder(parent, A + ".role", A + ".theory.xml", A + ".theory.xml.gz"):
        log("Role", getURI(path), "namespace")

def f_file(path, filename_real):
    full = os.path.join(path, filename_real)
    filename = filename_real.replace(".gz", "")
    name = filename.split(".", 1)[0]
    uri = getURI(path, name)
    # 1) Roles
    if filename.endswith(".theory.xml"):
        log("Role", uri, "file")
        # 3) Oggetti
        processTheoryXML(full)
    elif filename.endswith(".role"):
        with open(full) as f:
            role = f.read().strip()
        log("Role", uri, role)
    # 2) Declarations/Defitions
    elif filename.endswith(".con.xml"):
        if not in_folder(path, filename[:-8]+".con.body.xml", filename[:-8]+".con.body.xml.gz"):
            log("Declared", uri+".con")
    elif filename.endswith(".con.body.xml"):
        log("Defined", uri+".con")
    # 4) Size
    r = re_size.search(filename)
    if r:
        size = os.stat(full).st_size
        uri = uri + "." + r.group(1)
        log("Size", uri, str(size))
        # Add to database
        if not filename.endswith(".body.xml"):
            if name not in db:
                db[name.lower()] = []
            db[name.lower()].append((path, uri))

#
def try_match_aux(path, pre):
    path = path.strip("/").lower().split("/")
    print("try_match_aux", path, pre)
    j = 0
    i = 0
    while i < len(pre) and j < len(path):
        if pre[i] == path[j]:
            i += 1
        else:
            j += 1
    return (i == len(pre))

def try_match(list, pre):
    result = None
    for x in list:
        path, uri = x
        if try_match_aux(path, pre):
            if result:
                return
            else:
                result = uri
    return result

def find_in_db(url):
    full = url.split("#", 1)
    if len(full) != 2: return
    full = full[0][:-5] + "." + full[1]
    full = full.lower().split(".")
    pre, name = full[:-1], full[-1]
    list = None
    try:
        list = db[name]
    except KeyError:
        print("[ERR]", "Doc", pre, name, "not in db")
        return
    uri = try_match(list, pre)
    if uri:
        log("Doc", uri, url)
    else:
        print("[ERR]", "Doc", pre, name, "not found")

def doc(path, prefix):
    with open(path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            i = line.find('<a href="' + prefix)
            if i != -1:
                href = line[i:].split('"')[1]
                print("Looking", href)
                find_in_db(href)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="outfile.txt", help="output file")
    parser.add_argument("--doc", type=str, help="Path to index.html")
    args = parser.parse_args()
    with open(args.out, "w") as outfile:
        print(">>> Walking directories")
        walk(f_file, f_dir, ".")
        if args.doc:
            print(">>> Processing index.html")
            doc(args.doc, "")
