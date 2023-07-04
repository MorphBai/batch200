import pandas as pd
import requests

def check_website_availability(file_path):
    results = []
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()

    for url in urls:
        # 检查是否为空，如果为空，则跳过
        if not url:
            continue

        # 检查是否为数字，如果是数字，说明是ip地址格式，则加上http://
        valid_url = url.split('.')[0]
        if valid_url.isdigit():
            url = 'http://' + url
        
        # 检查是否以http://或https://开头，如果不是，则加上https://
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        
        print(f"Checking {url}...")
        result = {}
        result['URL/IP'] = url
        try:
            response = requests.get(url, timeout=10, verify=False)  # verify=False表示不验证证书，出翔 InsecureRequestWarning 警告，可以忽略
            if response.status_code == 200:
                result['Status'] = 'Accessible'
            else:
                result['Status'] = f"Returned status code {response.status_code}"
        except requests.exceptions.RequestException as e:
            result['Status'] = f"Not accessible. Error: {str(e)}"
        results.append(result)

    save_results_to_csv(results)

def save_results_to_csv(results):
    df = pd.DataFrame(results)
    df.to_csv('results.csv', index=False)

# 提供包含网址的文本文件路径
file_path = './urls.txt'

# 检查文件是否存在
try:
    with open(file_path, 'r') as file:
        pass
except FileNotFoundError:
    print(f'File {file_path} not found.')
    input('Press any key to exit...')
    exit()

# 调用函数进行检测并保存结果
try:
    check_website_availability(file_path)
    print('Results saved to results.csv')
except Exception as e:
    print('Error:', str(e))

input('Press any key to exit...')

