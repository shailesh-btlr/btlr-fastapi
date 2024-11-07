import pyotp
import secrets


def generate_otp():
    secret_key = pyotp.random_base32()
    hotp = pyotp.HOTP(secret_key, digits=5)
    otp = hotp.at(secrets.randbelow(10**6))
    return otp