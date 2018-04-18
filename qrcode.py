import sys
sys.path.append("lib/qrcode")
import QrCode
import logging

logger = logging.getLogger('wechat')

def scan(file_path):
    result = QrCode.scan(file_path)
    if not result:
        logger.error('qrcode scan failed!')
        return None 
    return result[0].decode('utf-8')

if __name__ == '__main__':
    print(scan(sys.argv[1]))