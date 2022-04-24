<?php

/**
 * @package IPP project 2022 - test.php
 * @author Vilem Gottwald
 */

require_once __DIR__. '/ReturnValues.php';
require_once __DIR__. '/TestTypes.php';

/**
 * Class for test.php command lines arguments processing. Script settings are saved into public properties.
 */
class CLA_GetSettings
{
    /**
     * Public properties for storing script settings.
     */
    public $directory = __DIR__;
    public $parseScript = __DIR__. '/parse.php';
    public $intScript =  __DIR__. '/interpret.py';
    public $jexampath = '/pub/courses/ipp/jexamxml/';
    public $jexamxml = '/jexamxml.jar';
    public $options = '/options';
    public $testType = TestTypes::BOTH;
    public $recursive = false;
    public $noclean = false;

    /**
     * Parses command line arguments and saves settings into public properties.
     */
    function __construct()
    {
        $longOptions = array(   "help",
                                "directory:",
                                "recursive",
                                "parse-script::",
                                "int-script::",
                                "parse-only",
                                "int-only",
                                "jexampath:",
                                "noclean"           );

        $options = getopt("", $longOptions);
        global $argc;
        $validOptsCount = 0;

        if ($options === false)
        {
            exit(ReturnValues::INTERNAL_ERR);
        }

        foreach ($options as $opt)
        {
            if (is_array($opt))
            {
                fwrite(STDERR, "ERROR: multiple occurrence of a certain parameter is not supported\n");
                exit(ReturnValues::PARAMETER_ERR);
            }
            $validOptsCount++;
        }

        if (($argc - 1) !== $validOptsCount)
        {
            fwrite(STDERR, "ERROR: unknown parameter\n");
            exit(ReturnValues::PARAMETER_ERR);
        }

        if(array_key_exists("help", $options))
        {
            if ($validOptsCount == 1)
            {
                $this->printHelp();
                exit(ReturnValues::SUCCESS);
            }
            else
            {
                fwrite(STDERR, "ERROR: invalid parameters combination\n");
                exit(ReturnValues::PARAMETER_ERR);
            }
        }

        if(array_key_exists("parse-only", $options))
        {
            if (array_key_exists("int-only", $options) or array_key_exists("int-script", $options))
            {
                fwrite(STDERR, "ERROR: invalid parameters combination\n");
                exit(ReturnValues::PARAMETER_ERR);    
            }
            $this->testType = TestTypes::PARSER;
        }
        else if (array_key_exists("int-only", $options))
        {
            if (array_key_exists("parse-script", $options) or array_key_exists("jexampath", $options)) 
            { // invalid combination with "parse-only" already checked in previous if 
                fwrite(STDERR, "ERROR: invalid parameters combination\n");
                exit(ReturnValues::PARAMETER_ERR);    
            }
            $this->testType = TestTypes::INTERPRET;
        }
        
        $this->recursive = array_key_exists("recursive", $options);
        $this->noclean = array_key_exists("noclean", $options);

        if(array_key_exists("directory", $options))
        {
            $this->checkPathExists($options["directory"]);
            $this->directory = $options["directory"];
        }
        if(array_key_exists("int-script", $options))
        {
            $this->checkPathExists($options["int-script"]);
            $this->intScript = $options["int-script"];
        }
        if(array_key_exists("parse-script", $options))
        {
            $this->checkPathExists($options["parse-script"]);
            $this->parseScript = $options["parse-script"];
        }
        if(array_key_exists("jexampath", $options))
        {
            $this->checkPathExists($options["jexampath"]);
            $this->jexampath = $options["jexampath"];
        }
    }

    /**
     * Check whether file or directory exists, if not exits with PATH_ERR error code.
     * @param string $path path to file or directory 
     */
    private function checkPathExists($path)
    {
        if(!file_exists($path))
        {
            fwrite(STDERR, "ERROR: invalid file or directory path\n");
            exit(ReturnValues::PATH_ERR);
        }
    }
    /**
     * Prints help for test.php.
     */
    private function printHelp()
    {
        echo "Usage: php8.1 test.php \n";
        echo "Search current directory for parse.php and interpret.py tests and perform testing.\n";
        echo "Test results are outputed to standard output in HTML 5 format.\n";
        echo "\n";
        echo "  --directory=path     search for tests in directory given in 'path'\n";
        echo "  --recursive          tests will also be recursively search in the specified directory subdirectories\n"; 
        echo "  --parse-script=file  file with PHP 8.1 parser script given in 'file' (default: parse.php located in current directory) \n"; 
        echo "  --int-script=file    file with Python 3.8 interpreter script given in 'file' (default: interpret.py located in current directory) \n"; 
        echo "  --parse-only         only parser script will be tested\n"; 
        echo "  --int-only           only interpreter script will be tested\n"; 
        echo "  --jexampath=path     path to directory containing jexamxml.jar and options files (default: /pub/courses/ipp/jexamml/)\n"; 
        echo "  --noclean            temporary files with intermediate results wil not be deleted\n"; 
    }
}
?>