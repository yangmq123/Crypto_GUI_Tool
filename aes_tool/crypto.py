"""AES-GCM 加解密模块

提供密钥生成、加密、解密功能。
- 密钥：由大小写字母和符号组成的 32 字节随机字符串（AES-256，256 位）
- 加密：输入文本，输出 Base64 字符串（包含随机 nonce、认证标签与密文）
- 解密：输入 Base64 字符串，输出原始文本
"""
import base64
import secrets

from Crypto.Cipher import AES

# AES-256 密钥长度（字节）
KEY_BYTES = 32
# GCM 推荐 nonce 长度（字节）
NONCE_BYTES = 12
# GCM 认证标签长度（字节）
TAG_BYTES = 16


def generate_key(length=KEY_BYTES):
    """生成随机密钥字符串，由大小写字母和符号组成，共 length 个字符（32 字节 = AES-256）。"""
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?/~"
    digits = "0123456789"
    alphabet = upper + lower + symbols+digits

    # 保证至少包含一个大写字母、一个小写字母和一个符号
    chars = [secrets.choice(upper), secrets.choice(lower), secrets.choice(symbols), secrets.choice(digits)]
    chars += [secrets.choice(alphabet) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def _to_key_bytes(key):
    if isinstance(key, str):
        key = key.encode("utf-8")
    if len(key) != KEY_BYTES:
        raise ValueError("密钥必须为32字节(256位)")
    return key


def encrypt(plaintext, key):
    """使用 AES-GCM 加密文本，返回 Base64 字符串。"""
    key_bytes = _to_key_bytes(key)
    nonce = secrets.token_bytes(NONCE_BYTES)
    cipher = AES.new(key_bytes, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
    return base64.b64encode(nonce + tag + ciphertext).decode("ascii")


def decrypt(ciphertext_b64, key):
    """使用 AES-GCM 解密 Base64 密文，返回文本。"""
    key_bytes = _to_key_bytes(key)
    raw = base64.b64decode(ciphertext_b64)
    if len(raw) < NONCE_BYTES + TAG_BYTES:
        raise ValueError("密文格式不正确")

    nonce = raw[:NONCE_BYTES]
    tag = raw[NONCE_BYTES:NONCE_BYTES + TAG_BYTES]
    ciphertext = raw[NONCE_BYTES + TAG_BYTES:]

    cipher = AES.new(key_bytes, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode("utf-8")
