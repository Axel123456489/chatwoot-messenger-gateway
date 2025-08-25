import secrets


def main():
    webhook_id = secrets.token_hex(32)  # 32 байта = 256 бит
    print(webhook_id)


if __name__ == "__main__":
    main()
