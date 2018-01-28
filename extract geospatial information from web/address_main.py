# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 21:56:58 2017

@author: yangpuhai
"""
import acquire_addresses as acq_addr

test_region_dir=['San Francisco2','Chicago2','New York2','Houston']

street_type_file='street_type'
type_file='types'

def main():
    for re_dir in test_region_dir:
        acq_addr.load_file_data(re_dir,'street',street_type_file,'city','state','country',type_file)
        acq_addr.acquire_url()
        acq_addr.acquire_web()
        acq_addr.acquire_address()
        acq_addr.address_types_csv()



if __name__ == '__main__':
    main()