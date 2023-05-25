# IPP project 2

## PHP tester - folder ./test



Searches current directory for parse.php and interpret.py tests and perform testing.
Test results are outputed to standard output in HTML 5 format.

    Usage: php8.1 test.php 
        --directory=path     search for tests in directory given in 'path'
        --recursive          tests will also be recursively search in the specified directory subdirectories 
        --parse-script=file  file with PHP 8.1 parser script given in 'file' (default: parse.php located in current directory)  
        --int-script=file    file with Python 3.8 interpreter script given in 'file' (default: interpret.py located in current directory)  
        --parse-only         only parser script will be tested 
        --int-only           only interpreter script will be tested 
        --jexampath=path     path to directory containing jexamxml.jar and options files (default: /pub/courses/ipp/jexamml/) 
        --noclean            temporary files with intermediate results wil not be deleted 


## Python interpret - folder ./interpret

Loads XML representation of an IPPcode2022 program, interprets this program and prints output to standard output.


    Usage: python3.8 interpret.py
        --source=file   source file with program XML representation
        --input=file    file with input for the interpretation itself
        One of these parameters has to be present.
        If file parameter missing, standard input is used instead of it
