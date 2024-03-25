# 导入所需模块和库
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import random
import string

'''
function getAesString(data, key0, iv0) {
    key0 = key0.replace(/(^\s+)|(\s+$)/g, "");
    var key = CryptoJS.enc.Utf8.parse(key0);
    var iv = CryptoJS.enc.Utf8.parse(iv0);
    var encrypted = CryptoJS.AES.encrypt(data, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString();
}
function encryptAES(data, aesKey) {
    if (!aesKey) {
        return data;
    }
    var encrypted = getAesString(randomString(64) + data, aesKey, randomString(16));
    return encrypted;
}
var $aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
var aes_chars_len = $aes_chars.length;
function randomString(len) {
    var retStr = '';
    for (i = 0; i < len; i++) {
        retStr += $aes_chars.charAt(Math.floor(Math.random() * aes_chars_len));
    }
    return retStr;
}'''


# AES 加密函数
def getAesString(data, key0, iv0):
    """
    Encrypts the input data using the AES algorithm with the provided key and IV.

    Args:
        data (str): The data to be encrypted.
        key0 (str): The key used for encryption.
        iv0 (str): The initialization vector used for encryption.

    Returns:
        str: The base64 encoded encrypted data.
    """
    # 去除密钥两端的空白字符
    key0 = key0.strip()
    # 将密钥和初始向量转换为 UTF-8 编码
    key = key0.encode('utf-8')
    iv = iv0.encode('utf-8')

    # 使用 PKCS7 填充方案对输入数据进行填充
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()

    # 创建 AES 加密器并进行加密
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    # 将加密后的数据进行 Base64 编码并返回
    return base64.b64encode(encrypted).decode('utf-8')


# AES 加密调用函数
def encryptAes(data, aes_key):
    """
    Login Encrypts the input data using the AES algorithm with the provided key.
    Encrypts the given data using AES encryption.

    Args:
        data: The data to be encrypted.
        aes_key: The AES encryption key.

    Returns:
        str: The encrypted data.
    """
    # 如果 AES 密钥不存在，则直接返回原始数据
    if not aes_key:
        return data
    # 生成一个随机字符串并与原始数据拼接
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    data_to_encrypt = random_str + data

    # 调用 AES 加密函数对拼接后的数据进行加密并返回
    encrypted = getAesString(data_to_encrypt, aes_key,
                             ''.join(random.choices(string.ascii_letters + string.digits, k=16)))
    return encrypted
