"""
Written by Carina Nilsson, February 2021, cnl@bth.se
"""
import sys
import os
import time
import logging
import pylint.lint
import numpy as np

from heapsort import heapsort
from quicksort import quicksort
from insertionsort import insertionsort

# check if Python version is valid for this script
if sys.version < '3.7':
    print('Your Python version is old. It is ' +
          sys.version + ' . Upgrade to at least 3.7')
    sys.exit(1)

# initiations
NEWLINE = '\n'
LINT_THRESHOLD = 8.0
FUNC_LIST = ['insertionsort', 'quicksort', 'heapsort']
LOG_LEVEL = 'INFO'  # Also DEBUG, INFO, WARNING, ...

# Small data sets
# TEST_DATA_FILES = ['1000(0,1000).txt', '1000(0,100000).txt',
#                    '1000(0,10000000).txt', '10000(0,1000).txt',
#                    '10000(0,100000).txt', '10000(0,10000000).txt']

# Large data sets, takes quite a while to run
# TEST_DATA_FILES = ['50000(0,1000).txt', '50000(0,100000).txt',
#                    '50000(0,10000000).txt', '100000(0,1000).txt',
#                    '100000(0,100000).txt', '100000(0,10000000).txt']

# Almost sorted datasets
TEST_DATA_FILES = [
    '1000(0,10000).txt', '10000(0,10000).txt', '50000(0,10000).txt']


# functions
def check_functions():
    """Checks if all required functions are implemented"""
    log.info(
        f'\nTesting if the required functions are implemented. ({FUNC_LIST})')
    print(f'\nTesting if the required functions are implemented.({FUNC_LIST})')
    for func in FUNC_LIST:
        if func not in globals():
            print(f'Test failed!\nThe function {func}() is missing.')
            sys.exit(1)

    log.info('All required functions are there.\n')
    print('All required functions are there.\n')
    return True


def check_sorting(sortfunc):
    """Checks if sorting completes correctly for a sort function"""
    input_list = np.random.randint(-1000, 1000, size=10).tolist()
    input_copy = input_list[:]
    result = sortfunc(input_list)
    if result is None:
        sorted_list = input_list
    else:
        sorted_list = result
    for i in range(0, len(sorted_list)-1):
        if sorted_list[i] > sorted_list[i+1]:
            print('\nTest failed! Sortorder corrupt.\n')
            log.info('Sortorder corrupt.\n')
            return False
    for item in input_copy:
        if (sorted_list.count(item) != input_copy.count(item) or
                len(sorted_list) != len(input_copy)):
            print('\nTest failed! Elements are missing or duplicated\n')
            log.info('Elements are missing or duplicated\n')
            return False
    return True


def test_code_quality():
    """Checks pylint score against LINT_THRESHOLD"""
    print('\nChecking code quality by pylint score, 8.0 is minimum to pass\n')
    log.info('\nChecking code quality by pylint score, 8.0 is minimum to pass')
    stdout = sys.stdout
    outfile = open('pylint_report.txt', 'w')
    for func in FUNC_LIST:
        sys.stdout = outfile
        run = pylint.lint.Run(
            [func + '.py'], exit=False)
        score = run.linter.stats['global_note']
        if score < LINT_THRESHOLD:
            log.info(
                f'The {func} pylint score is only {score:.2f}, at least {LINT_THRESHOLD} required')
            sys.stdout = stdout
            outfile.close()
            print(
                f'Test failed!\nThe {func} pylint score is only {score:.2f},',
                f' at least {LINT_THRESHOLD} required')
            print('\nDetailed report can be viewed in pylint_report.txt\n')
            sys.exit(1)
        else:
            sys.stdout = stdout
            print(f'{func} lint score is {score:.2f}')
    log.info('Lint score OK')
    print('\nLint score OK. Detailed report can be viewed in pylint_report.txt\n')


def test_sorting(functions, sortfunc_names):
    """Calls sort test for all sort functions"""
    for i, func in enumerate(functions):
        if check_sorting(func):
            log.info('Correct sorting: ' + sortfunc_names[i])
            print('Correct sorting: ' + sortfunc_names[i])
        else:
            log.info('Failed sorting: ' + sortfunc_names[i])
            print('Failed sorting: ' + sortfunc_names[i])
            sys.exit(1)


def test_performance(functions, sortfunc_names):
    """Performance test on test data sets < 10 000 elements"""
    summary = 'sorted refers to Python built-in sorted function\n\n'
    m_file = input("Give filename for saved measurements: ")
    log_handle = open(m_file, 'w')
    log_handle.write(summary)
    log_handle.close()
    max_check_index = -1
    for i, file_name in enumerate(TEST_DATA_FILES):
        if int(file_name.split('(')[0]) > 10000:
            break
        max_check_index = i

    for test_nr, file_name in enumerate(TEST_DATA_FILES):
        summary = '\n'
        with open('Testdata/'+file_name, 'r') as file:
            num_list = list(map(int, file.readlines()))

        nr_of_items = file_name.split('(')[0]
        limit = file_name.split(',')[1].split(')')[0]
        summary += f'Sorting {nr_of_items} items, values (0,{limit})\n'
        summary += f'{"Algorithm":25} {"Time (seconds)"}\n'
        summary += '-'*42 + '\n'
        for i, func in enumerate(functions):
            test_data = num_list.copy()
            timestamp_before = time.perf_counter()
            func(test_data)
            timestamp_after = time.perf_counter()
            sec = timestamp_after - timestamp_before
            summary += f'{sortfunc_names[i]:25} {sec:.4}\n'
            log_handle = open(m_file, 'a')
            log_handle.write(summary)
            log_handle.close()
            summary = ''
            if test_nr <= max_check_index and sec > 5:
                print(
                    'Test failed!\nToo slow, 5 seconds is maximum for up to 10 000 elements\n')
                log.info(
                    f'{sortfunc_names[i]} sorted too slow ({sec:.4}) seconds, 5 seconds is maximum')
                sys.exit(1)
        if test_nr == max_check_index:
            print('Performance check OK, all timing requirements met')

    log.info('Performance check OK, all requirements met')


def create_report(sortfunc_list):
    """Calls all tests and creates/displays report"""
    sortfunc_names = []
    for func in sortfunc_list:
        sortfunc_names.append(func.__name__)
    check_functions()
    test_sorting(sortfunc_list, sortfunc_names)
    test_performance(sortfunc_list, sortfunc_names)
    test_code_quality()
    print('\nAll tests passed successfully!')
    log.info('\nAll tests passed successfully!')


if __name__ == '__main__':
    directory = os.path.dirname(os.path.abspath(__file__))
    log = logging.getLogger(__name__)
    logging.basicConfig(filename=directory+'/test.log', level=os.environ.get('LOGLEVEL', LOG_LEVEL),
                        filemode='w',
                        format='\n%(levelname)-4s [L:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S')
    sys.setrecursionlimit(10000)
    func_list = [sorted, quicksort, heapsort, insertionsort]
    create_report(func_list)
