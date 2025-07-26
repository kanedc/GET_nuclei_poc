import requests
import zipfile
import os
import stat
import subprocess

def get_latest_release():
    url = "https://api.github.com/repos/projectdiscovery/nuclei/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch latest release")

def download_file(url, dest):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        raise Exception(f"Failed to download file: {url}")

def unzip_file(zip_path, extract_to='.'):
    with zipfile.ZipFile(zip_path,'r') as zip_ref:
        zip_ref.extractall(extract_to)

def main():
    release = get_latest_release()
    assets = release['assets']
    
    download_url = None
    for asset in assets:
        if 'linux' in asset['name'] and 'amd64' in asset['name'] and asset['name'].endswith('.zip'):
            download_url = asset['browser_download_url']
            binary_name = asset['name'].replace('.zip','')
            break

    if not download_url:
        raise Exception("Linux amd64 ZIP asset not found in the latest release")

    print(f"Downloading from {download_url}")

    dest_file = 'nuclei.zip'
    download_file(download_url, dest_file)

    print("Downloaded Nuclei ZIP file")

    unzip_file(dest_file)
    print("Unzipped Nuclei")

    command = ['chmod','+x','./nuclei']
    try:
        result = subprocess.run(command,check=True,capture_output=True,text=True)
        print(f"命令'{' '.join(command)}'执行成功。")
    except FileNotFoundError:
    print("错误：'chmod' 命令未找到。请确保你在一个类 Unix 系统 (Linux, macOS) 上运行。")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，返回码: {e.returncode}")
        print("错误信息:", e.stderr)

if __name__ == "__main__":
    main()
