import random
import des
import datetime


def generate_random_passwords(N: int, start_date: datetime, end_date: datetime) -> list[str]:
    passwords = []
    for i in range(N):
        random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        encrypted_password = des.encrypt(random_date.strftime("%Y%m%d"))
        passwords.append(encrypted_password)

    return passwords


if __name__ == '__main__':
    start_date = datetime.date(1900, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    passwords = generate_random_passwords(10, start_date, end_date)
    print(passwords)
