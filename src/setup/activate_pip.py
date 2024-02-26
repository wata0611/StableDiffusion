import os, subprocess, sys

ROOT_DIR = os.getenv('ROOT_DIR')

pth_file_content = [
    "python310.zip\n",
    ".\n",
    "\n",
    "# Uncomment to run site.main() automatically\n",
    "#import site"
]

def main():
    pth_file = os.path.join(ROOT_DIR, 'python', 'python310._pth')
    with open(pth_file, mode='w', encoding='utf-8', newline='\n') as f:
        f.writelines(pth_file_content)

    subprocess.run(["curl", "-sSL", "https://bootstrap.pypa.io/get-pip.py", "-o", f"{ROOT_DIR}python\get-pip.py"])

    subprocess.run([sys.executable, f"{ROOT_DIR}python\get-pip.py"])

    os.remove(pth_file)

if __name__ == '__main__':
    main()