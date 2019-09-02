#!/usr/bin/env python3

'''
Finder is part of https://github.com/internetwache/GitTools

Developed and maintained by @gehaxelt from @internetwache
updated by  @no_kriminality

Use at your own risk. Usage might be illegal in certain circumstances.
Only for educational purposes!
'''

import argparse
from functools import partial
from multiprocessing import Pool
from urllib.request import urlopen
from urllib.error import HTTPError
import concurrent.futures
import asyncio
import sys
import time
import requests





def findgitrepos(domains, out_file):
    now = time.time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
    loop = asyncio.get_event_loop()


    async def check_domains(domains):

        def single_domain(domain):
            domain = domain.strip()
            try:
                r = requests.get(''.join(['http://', domain, '/.git/HEAD']), timeout=5)
                r = r.text
            except:
                r = ''
            if 'refs/heads' not in r:
               # print (domain + " NOT FOUND")
                return (domain,'Not found')
            else:
                print (domain, " FOUND")
                with open(out_file, 'a') as file_handle:
                    file_handle.write(''.join([domain, '\n']))
                return (domain + 'Found')
        futures = [loop.run_in_executor(executor,single_domain, domain) for domain in domains]
        await asyncio.wait(futures)

    loop.run_until_complete(check_domains(domains))



def read_file(filename):
    with open(filename) as file:
        return file.readlines()

def main():
    print("""
###########
# Finder is part of https://github.com/internetwache/GitTools
#
# Developed and maintained by @gehaxelt from @internetwache
# v2 is implemented by @no_kriminality
#
# Use at your own risk. Usage might be illegal in certain circumstances.
# Only for educational purposes!
###########
""")

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', default='input.txt', help='input file')
    parser.add_argument('-o', '--outputfile', default='output.txt', help='output file')
    args = parser.parse_args()

    domain_file = args.inputfile
    output_file = args.outputfile

    d = read_file(domain_file)
    findgitrepos(d, output_file)



if __name__ == '__main__':
    main()
