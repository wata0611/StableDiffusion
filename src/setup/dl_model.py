import urllib.request, urllib.error, os, sys
from concurrent.futures import ThreadPoolExecutor

MAX_WORKER = 8
ROOT_DIR = os.getenv('ROOT_DIR')

# ダウンロードしたいモデルのURLと保存先の情報を取得
def load_dl_model_list():
    dl_model_info = {}
    with open(os.path.join(ROOT_DIR, 'dl_model_list.txt'), encoding='utf-8') as f:
        for line in f.readlines():
            url, save_path = line.strip().split(':')
            save_path = [ROOT_DIR]+save_path.split('/')
            save_path = os.path.join(*save_path)
            dl_model_info[url] = save_path
    return dl_model_info

# ファイル1つのダウンロード
def download_file(url:str, save_path:str):
    try:
        if os.path.exists(save_path):
            print(f"this file is exists {save_path}")
            return True
        with urllib.request.urlopen(url) as web_file:
            with open(save_path, 'wb') as local_file:
                local_file.write(web_file.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP ERROR: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR", file=sys.stderr)
        return False
    return True

def main():
    # モデルディレクトリの生成
    os.makedirs(os.path.join(ROOT_DIR, 'models', 'StableDiffusion'), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, 'models', 'LoRA'), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, 'models', 'ControlNet'), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, 'models', 'VAE'), exist_ok=True)

    # モデルのダウンロードを並列に実行
    dl_model_info = load_dl_model_list()
    with ThreadPoolExecutor(max_workers=8) as threads:
        for url, save_path in list(dl_model_info.items()):
            threads.submit(download_file, url, save_path)
