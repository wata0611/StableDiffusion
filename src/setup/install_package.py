import subprocess, sys, os, site, importlib

PIP = os.getenv('PIP')

def main():
    subprocess.run([sys.executable, PIP, 'install', 'torch==2.1.0', 'torchvision==0.16.0', '--index-url', 'https://download.pytorch.org/whl/cu121'])
    importlib.reload(site)

    subprocess.run([sys.executable, PIP, 'install', '-r', 'requirements.txt'])
    importlib.reload(site)