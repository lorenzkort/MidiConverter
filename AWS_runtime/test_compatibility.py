import requests
import tempfile
import subprocess
import os

# TensorFlow Lite PyPI project name
PROJECT_NAME = 'tflite-runtime'

# Function to fetch available versions of TensorFlow Lite from PyPI
def fetch_tflite_versions():
    url = f'https://pypi.org/pypi/{PROJECT_NAME}/json'
    response = requests.get(url)
    response.raise_for_status()  # Raises a HTTPError if the response status code is 4XX/5XX
    data = response.json()
    return data['releases'].keys()

# Function to download a wheel file and check for GLIBC version requirement
def check_glibc_requirement(version):
    url = f'https://pypi.org/pypi/{PROJECT_NAME}/{version}/json'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # Find the wheel file URL, assuming Linux x86_64 platform
    wheel_url = None
    for file_info in data['urls']:
        if file_info['packagetype'] == 'bdist_wheel' and 'linux_x86_64' in file_info['filename']:
            wheel_url = file_info['url']
            break
    
    if not wheel_url:
        return None
    
    # Download the wheel file
    with requests.get(wheel_url, stream=True) as r:
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            for chunk in r.iter_content(chunk_size=8192):
                fp.write(chunk)
            temp_filename = fp.name
    
    try:
        # Check the wheel file for GLIBC version requirement using auditwheel
        result = subprocess.run(['auditwheel', 'show', temp_filename], capture_output=True, text=True)
        output = result.stdout
        # Extract the GLIBC version requirement
        if 'GLIBC' in output:
            return output.split('GLIBC')[1].split(' ')[0].strip()
        else:
            return 'No GLIBC requirement found'
    finally:
        os.remove(temp_filename)

# Main script logic
def main():
    versions = fetch_tflite_versions()
    for version in versions:
        print(f'Checking TensorFlow Lite version {version}...')
        glibc_requirement = check_glibc_requirement(version)
        if glibc_requirement:
            print(f'Version {version} GLIBC requirement: {glibc_requirement}')
        else:
            print(f'Version {version} has no specific GLIBC requirement or could not be checked.')

if __name__ == '__main__':
    main()
