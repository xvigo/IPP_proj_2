<?php

/**
 * @package IPP project 2022 - test.php
 * @author Vilem Gottwald
 */


require_once __DIR__. '/HtmlSnippets.php';
require_once __DIR__. '/TestTypes.php';

/**
 * Class for generating output HTML with test results.
 */
class HtmlWriter
{

    /**
     * Prints output html head section.
     */
    static function printHead()
    {
        echo HTML::$head;
    }

    /**
     * Prints output html body start section and main header containing title.
     */
    static function printHeader()
    {
        echo HTML::$header;
    }

    /**
     * Prints configutation details to output HTML.
     * @param $config configuration object created by CLA_GetSettings 
     */
    static function printConfig($config)
    {
        echo HTML::$configStart;
        switch ($config->testType) {
            case TestTypes::BOTH:
                echo "          <li>parse-script: $config->parseScript</li>\n";
                echo "          <li>int-script: $config->intScript</li>\n";
                echo "          <li>jexampath: $config->jexampath</li>\n"; 
                break;
            case TestTypes::INTERPRET:
                echo "          <li>int-only</li>\n";
                echo "          <li>int-script: $config->intScript</li>\n";
                break;
            case TestTypes::PARSER:
                echo "          <li>parse-only</li>\n";
                echo "          <li>parse-script: $config->parseScript</li>\n";  
                echo "          <li>jexampath: $config->jexampath</li>\n"; 
                break;
        }
        echo "          <li>directory: $config->directory</li>\n";

        if ($config->recursive)
        {
            echo "          <li>recursive</li>\n";
        }

        if ($config->noclean)
        {
            echo "          <li>noclean</li>\n";
        }
        echo HTML::$configEnd;
    }

    /**
     * Prints testing summary to output HTML.
     * @param int $passedC nubber of passed tests
     * @param int $failedC number of failed tests
     */
    static function printSummary($passedC, $failedC)
    {
        $sum = $passedC + $failedC;
        $percentage = round($passedC / $sum * 100, 2);
        echo HTML::$summaryStart;
        echo "<div class='percentage'> $percentage% </div>\n";
        echo "<ul class='counts'>\n";
        echo "<li>Počet testů: $sum</li>\n";
        echo "<li>Celkem úspěšných: $passedC</li>\n";
        echo "<li>Celkem neúspěšných: $failedC</li>\n";
        echo HTML::$summaryEnd;
        echo HTML::$resultsHeader;
    }

    /**
     * Prints single test case result to output HTML.
     * @param $testResult TestResult object representing result of a single test
     */
    static function printTestcase($testResult)
    {
        echo "<div class='result $testResult->type'>\n";
        echo "    <p class='order'>$testResult->order.</p>\n";
        echo "    <div class='description'>\n";
        echo "        <p>Umístění: $testResult->testDir</p>\n";
        echo "        <p>Název: $testResult->testName</p>\n";
        if ($testResult->type === "failed")
        {
            if($testResult->expRC)
            {
                echo "        <p class='error'>Chyba: Rozdílné návratové kódy (očekávaný: $testResult->expRC, reálný: $testResult->actRC)</p>\n";
            }
            else
            {
                echo "        <p class='error'>Chyba: Rozdílný výstup</p>\n";
            }
            echo "    </div>\n";
            echo "    <p class='type'>&#x274C;</p>\n";
        }
        else
        {
            echo "    </div>\n";
            echo "    <p class='type'>&#9989;</p>\n";
        }
        echo " </div>\n";
    }

    /**
     * Prints body and html end tag output HTML.
     */
    static function printHtmlEnd()
    {
        echo HTML::$pageEnd;
    }
}
?>