import time
import des
import json
import utils
import asyncio

import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List


def read_words_from_file() -> dict[str, str]:
    with open("words.json", 'r') as f:
        words = json.load(f)
    return words


def get_intervals(words: dict[str, str], n_threads: int) -> [[int, int]]:
    N = len(words)
    interval_size = N // n_threads
    intervals = []
    start_i = 0
    for _ in range(n_threads):
        end_i = start_i + interval_size
        if end_i > N:
            end_i = N - 1

        intervals.append([start_i, end_i])
        start_i = end_i + 1

    return intervals


def sequential_solver(words: dict[str, str]) -> None:
    for password, encrypted in words.items():
        enc_to_bin = utils.str_to_bin(encrypted)
        decrypted = des.decrypt(enc_to_bin)

        if password != decrypted:
            raise Exception(f"{password} and {decrypted} are not matching")


def parallel(words: dict[str, str], passwords: list[str], interval: [[int, int]]) -> None:
    start_i, end_i = interval[0], interval[1]

    for i in range(start_i, end_i):
        enc_to_bin = utils.str_to_bin(words[passwords[i]])
        decrypted = des.decrypt(enc_to_bin)

        if passwords[i] != decrypted:
            raise Exception(f"{password} and {decrypted} are not matching")


async def parallel_solver(words: dict[str, str], passwords: list[str], n_threads: int) -> None:
    intervals = get_intervals(words, n_threads)

    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_event_loop()
        calls: List[partial] = [partial(parallel, words, passwords, interval) for interval in intervals]
        call_coros = []
        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))

        await asyncio.gather(*call_coros)


async def main() -> None:
    times = {}
    speedups = {}
    n_tests = 10

    words = read_words_from_file()
    passwords = list(words)

    start = time.time()
    for i in range(n_tests):
        sequential_solver(words)
    end = time.time()
    seqElapsed = (end - start) / n_tests * 1000
    print(f'sequential time {seqElapsed} ms')

    times[1] = seqElapsed

    threads = [2, 4, 6, 8, 16, 32]
    for n_threads in threads:
        start = time.time()
        for i in range(n_tests):
            await parallel_solver(words, passwords, n_threads)

        end = time.time()
        parElapsed = (end - start) / n_tests * 1000
        speedup = seqElapsed / parElapsed
        print(f'{n_threads} threads time: {parElapsed} ms')
        print(f'{n_threads}  threads speed up: {speedup} ms')

        times[n_threads] = parElapsed
        speedups[n_threads] = speedup

    print(times)
    print(speedups)


if __name__ == '__main__':
    asyncio.run(main())
