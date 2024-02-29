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


def read_words():
    with open("words.json", 'r') as f:
        words = json.load(f)
    return words


def get_chunks(words):
    N = len(words)
    threads = 8
    interval_size = N // threads
    chunks = []
    start_i = 0
    for _ in range(threads):
        end_i = start_i + interval_size
        if end_i > N:
            end_i = N - 1

        chunks.append([start_i, end_i])
        start_i = end_i + 1

    return chunks


def sequential_solver(words):
    for password, encrypted in words.items():
        enc_to_bin = utils.str_to_bin(encrypted)
        decrypted = des.decrypt(enc_to_bin)

        if password != decrypted:
            raise Exception(f"{password} and {decrypted} are not matching")


def parallel(words, passwords, chunk):
    start_i, end_i = chunk[0], chunk[1]

    for i in range(start_i, end_i):
        enc_to_bin = utils.str_to_bin(words[passwords[i]])
        decrypted = des.decrypt(enc_to_bin)

        if passwords[i] != decrypted:
            raise Exception(f"{password} and {decrypted} are not matching")
    return True


async def parallel_solver(words, passwords):
    chunks = get_chunks(words)

    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_event_loop()
        calls: List[partial] = [partial(parallel, words, passwords, c) for c in chunks]
        call_coros = []
        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))

        await asyncio.gather(*call_coros)


async def main():
    words = read_words()
    passwords = list(words)

    start = time.time()
    sequential_solver(words)
    end = time.time()
    print(f'sequential time {end - start} s')

    start = time.time()
    await parallel_solver(words, passwords)
    end = time.time()
    print(f'parallel time {end - start} s')


if __name__ == '__main__':
    asyncio.run(main())
