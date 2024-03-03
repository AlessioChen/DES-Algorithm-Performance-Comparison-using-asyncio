# DES Algorithm Performance Comparison using asyncio

This project aims to compare the performance of sequential and parallel implementations of the Data Encryption Standard (DES) algorithm using the asyncio concurrent library in Python. The comparison focuses on decrypting a set of randomly generated passwords encrypted with DES.

## Overview
The project consists of two main components:

- Implementation: Sequential and parallel implementations of DES decryption algorithms are provided. The sequential approach decrypts passwords one after the other, while the parallel approach utilizes asyncio to execute decryption tasks concurrently across multiple threads.

- Evaluation: Performance evaluations are conducted to compare the execution times and scalability of the sequential and parallel implementations. Tests are performed with varying numbers of passwords and threads to analyze performance variations under different scenarios.

## Files
- main.py: Contains the main code for running the sequential and parallel implementations and conducting performance evaluations.
- des.py: Contains the implementations of encryption, decryption methods.
- words_gen.pt: Contains the script to randomly generate the input.
- utils.py: Utility functions for encryption, decryption, and other auxiliary tasks.
- report.pdf: file containing the detailed report of the project, including methodology, results, and conclusions.

## Requirements
Python 3.x
