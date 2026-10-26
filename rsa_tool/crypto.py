"""RSA 加解密模块

提供密钥生成、加密、解密功能。
- 加密：输入文本，输出 Base64 字符串
- 解密：输入 Base64 字符串，输出原始文本
"""
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

# 默认密钥长度（位）
DEFAULT_BITS = 2048


def generate_key_pair(bits=DEFAULT_BITS):
    """生成 RSA 密钥对，返回 (公钥PEM, 私钥PEM)。"""
    key = RSA.generate(bits)
    private_pem = key.export_key()
    public_pem = key.publickey().export_key()
    return public_pem, private_pem


def _max_chunk_size(key):
    """OAEP(SHA256) 下单次可加密的最大明文字节数。"""
    return key.size_in_bytes() - 2 * SHA256.digest_size - 2


def encrypt(plaintext, public_key):
    """使用公钥加密文本，返回 Base64 字符串。

    public_key 可为 PEM 字符串、PEM 字节串或 RSA 公钥对象。
    """
    if isinstance(public_key, RSA.RsaKey):
        key = public_key
    else:
        if isinstance(public_key, str):
            public_key = public_key.encode("utf-8")
        key = RSA.import_key(public_key)

    data = plaintext.encode("utf-8")
    if not data:
        return ""

    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    max_size = _max_chunk_size(key)
    encrypted = b"".join(
        cipher.encrypt(data[i:i + max_size])
        for i in range(0, len(data), max_size)
    )
    return base64.b64encode(encrypted).decode("ascii")


def decrypt(ciphertext_b64, private_key):
    """使用私钥解密 Base64 密文，返回文本。

    private_key 可为 PEM 字符串、PEM 字节串或 RSA 私钥对象。
    """
    if isinstance(private_key, RSA.RsaKey):
        key = private_key
    else:
        if isinstance(private_key, str):
            private_key = private_key.encode("utf-8")
        key = RSA.import_key(private_key)

    if not ciphertext_b64:
        return ""

    encrypted = base64.b64decode(ciphertext_b64)
    key_size = key.size_in_bytes()
    if len(encrypted) % key_size != 0:
        raise ValueError("密文长度与密钥长度不匹配，请检查私钥是否正确")

    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    decrypted = b"".join(
        cipher.decrypt(encrypted[i:i + key_size])
        for i in range(0, len(encrypted), key_size)
    )
    return decrypted.decode("utf-8")
