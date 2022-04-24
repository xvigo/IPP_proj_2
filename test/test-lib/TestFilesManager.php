<?php

/**
 * @package IPP project 2022 - test.php
 * @author Vilem Gottwald
 */

require_once(__DIR__. "/ReturnValues.php");

final class TestFilesManager
{
    /**
     * Scans directory( and possibly its subdirectories) and searches for .src files.
     * @param string $directory directory to scan
     * @param bool $recursive bool whether subdirectories should be scanned
     * @return array $files array of full paths to foud files containing only filename (without the .src extension)
     */
    public static function getTestsFromDir($directory, $recursive)
    {
        $files = [];
        foreach(scandir($directory) as $content)
        {
            if ( $content == "." or $content == "..")
            {
                continue;
            }

            $fullpath = $directory . '/' . $content;
            if (is_dir($fullpath))
            {
                if ($recursive)
                {
                    array_push($files, ...TestFilesManager::getTestsFromDir($fullpath, true));
                }
            } 
            else 
            {
                if (pathinfo($content, PATHINFO_EXTENSION) == "src")
                {
                    $files[] = $directory . '/' . pathinfo($content, PATHINFO_FILENAME);
                }
            }
        }
        return $files;
    }

    /**
     * Checks whether .rc, .in and .out test files exist, if not - creates them.
     * @param array $pathsWFilenames array containing full paths to test files without their extensions
     */
    public static function generateMissingTestFiles($pathsWFilenames)
    {
        foreach ($pathsWFilenames as $path)
        {
            TestFilesManager::createFile($path . ".rc", "0");
            TestFilesManager::createFile($path . ".in", "");
            TestFilesManager::createFile($path . ".out", ""); 
        }
    }

    /**
     * Creates file and writes string given as parameter into it.
     * If file allready exists, does nothing.
     * @param string $path full path to created file
     * @param string $text text to write into file
     */
    private static function createFile($path, $text)
    {
        if (file_exists($path))
        {
            return;
        }

        $file = fopen($path,"w");
        if ($file === false)
        {
            exit(ReturnValues::INTERNAL_ERR);
        }
        
        if (fwrite($file, $text) === false)
        {
            exit(ReturnValues::INTERNAL_ERR);
        }

        if (fclose($file) === false)
        {
            exit(ReturnValues::INTERNAL_ERR);
        }
    }
}

?>