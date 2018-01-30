# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 16:38:09 2017

@author: yangpuhai
"""
import acquire_place_name as apn

test_region_dir=['Chicago','Houston']

filter_words_file='filter_words'

def main():
    for re_dir in test_region_dir:
        print re_dir
        apn.load_file_data(re_dir,'city','state',filter_words_file)
        apn.new_acquire_titles_key_word()
        apn.new_acquire_place_name()
        apn.new_combine_place_name()
        

if __name__ == '__main__':
    main()