import des
import time
import utils
import asyncio
import datetime

from functools import partial
from asyncio.events import AbstractEventLoop
from words_gen import generate_random_passwords
from concurrent.futures import ProcessPoolExecutor


def read_password_from_file():
    with open('passwords.txt', 'r') as file:
        passwords = file.read().splitlines()

    return passwords


def get_dates() -> list[str]:
    date_range: list[str] = []
    for year in range(1900, 2025):
        for month in range(1, 13):
            for day in range(1, 32):
                date_range.append(f"{year:04d}{month:02d}{day:02d}")

    return date_range


def get_chunks(n_threads: int, dates: list[str]) -> list[list[int, int]]:
    N = len(dates)
    interval_size = N // n_threads
    intervals = []
    start_i = 0
    for _ in range(n_threads):
        end_i = start_i + interval_size
        if end_i > N:
            end_i = N - 1
        intervals.append(([start_i, end_i]))
        start_i = end_i + 1

    return intervals


def get_decrypted_passwords(encrypted_passwords: list[str]) -> list[str]:
    res = []
    for password in encrypted_passwords:
        res.append(des.decrypt(utils.str_to_bin(password)))

    return res


def sequential_brute_force(passwords: str, dates: list[str]) -> None:
    for password in passwords:
        for date in dates:
            encrypted = des.encrypt(date)
            if encrypted == password:
                print(f"Password found : {des.decrypt(utils.str_to_bin(encrypted))}")
                break


def parallel(password: str, chunk: [[int, int]], dates: list[str]) -> None:
    start_i, end_i = chunk[0], chunk[1]

    for i in range(start_i, end_i):
        encrypted = des.encrypt(dates[i])
        if encrypted == password:
            print(f"Password found: {des.decrypt(utils.str_to_bin(encrypted))}")
            break


async def parallel_crack(passwords: list[str], dates: list[str], n_threads: int) -> None:
    for password in passwords:
        await parallel_brute_force(password, dates, n_threads)


async def parallel_brute_force(password: str, dates: list[str], n_threads: int) -> None:
    chunks = get_chunks(n_threads, dates)

    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        calls: List[partial] = [partial(parallel, password, chunk, dates) for chunk in chunks]
        call_coros = []
        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))

        await asyncio.gather(*call_coros)


async def main() -> None:
    N_TESTS = 10
    N_TO_CRACK = 1

    start_date = datetime.date(1900, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    dates = get_dates()
    encrypted_passwords = []
    for i in range(N_TESTS):
        encrypted_passwords.append(generate_random_passwords(N_TO_CRACK, start_date, end_date))

    times = []
    speedups = []

    start = time.time()
    for i in range(N_TESTS):
        sequential_brute_force(encrypted_passwords[i], dates)
    end = time.time()
    seqElapsed = (end - start) / N_TESTS * 1000
    print(f'sequential time {seqElapsed} ms\n')
    times.append(seqElapsed)

    threads = [2, 4, 6, 8, 16, 32]
    for n_thread in threads:
        start = time.time()
        for i in range(N_TESTS):
            await parallel_crack(encrypted_passwords[i], dates, n_thread)
        end = time.time()
        parElapsed = (end - start) / N_TESTS * 1000
        speedup = seqElapsed / parElapsed
        print(f'{n_thread} threads time: {parElapsed} ms')
        print(f'{n_thread}  threads speed up: {speedup} ms')

        times.append(parElapsed)
        speedups.append(speedup)

    print(times)
    print(speedups)


if __name__ == '__main__':
    asyncio.run(main())
