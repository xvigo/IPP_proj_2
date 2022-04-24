<?php

/**
 * @package IPP project 2022 - test.php
 * @author Vilem Gottwald
 */

require_once(__DIR__. "/TestTypes.php");
require_once(__DIR__. "/HtmlWriter.php");
/**
 * Class for representing single test case result.
 */
final class TestResult
{
    public $order;
    public $type;
    public $testName;
    public $testDir;
    public $expRC;
    public $actRC;

    /**
     * Creates TestResult object.
     * @param int $order - order of test case
     * @param string $filePath - filepath to test file
     * @param bool $hasPassed - marks whether test has passed or not
     * @param $expRc - expected return code (in case of different return codes)
     * @param $actRc - actual return code (in case of different return codes)
     */
    public function __construct($order, $filePath, $hasPassed, $expRC=NULL, $actRC= NULL)
    {
        $this->order=$order;
        $info = pathinfo($filePath);
        $this->testName = $info['filename'];
        $this->testDir = $info['dirname'] . "/";
        $this->type = $hasPassed ? "passed" : "failed";
        $this->expRC = is_null($expRC) ? NULL : $expRC;
        $this->actRC = is_null($actRC) ? NULL : $actRC;
    }
}

/**
 * Class for performing the testing itself.
 */
final class Tester
{
    public $testResults;
    public $passedCount;
    public $failedCount;
    private $counter;

    public function __construct()
    {
        $this->counter = 1;
        $this->passedCount = 0;
        $this->failedCount = 0;
        $this->testResults = [];
    }

    /**
     * Prints HTML with test results to standdard output.
     * @param $config - object containing current testing configurantion
     */
    public function printTestsHtml($config)
    {
        HtmlWriter::printHead();
        HtmlWriter::printHeader();
        HtmlWriter::printConfig($config);
        HtmlWriter::printSummary($this->passedCount, $this->failedCount);
        foreach ($this->testResults as $test)
        {
            HtmlWriter::printTestcase($test);
        }
        HtmlWriter::printHtmlEnd();
    }

    /**
     * Performs tests given in testFiles and stores results.
     * @param $config - object containing current testing configurantion
     * @param $testFiles - list of files containig tests
     */
    public function test($config, $testFiles)
    {
        switch($config->testType)
        {
            case TestTypes::BOTH:
                $this->bothTest($config, $testFiles);
                break;
            case TestTypes::PARSER:
                $this->parserTest($config, $testFiles);
                break;
            case TestTypes::INTERPRET:
                $this->interpretTest($config, $testFiles);
                break;
        }
    }

    /**
     * Performs parser tests and after that interpreter tests.
     * @param $config - object containing current testing configurantion
     * @param list $testFiles - list of files containig tests
     */
    private function bothTest($settings, $testFiles)
    {
        foreach($testFiles as $test)
        {   
            $expRC = file_get_contents($test . ".rc");
            if($expRC === "0")
            { // succes return code - compare outputs
                $command = "php8.1 $settings->parseScript < $test.src | python3.8 $settings->intScript --input=$test.in >$test.intOut";
                exec($command, $output, $actRC);

                if($expRC == $actRC)
                { // identical return codes - compare outputs
                    $command = "diff " . $test . ".intOut " . $test . ".out ";
                    exec($command, $output, $diffRC); 
                    $this->checkDiffRetCode($diffRC, $test);
                }
                else
                {  // different return codes
                    $this->newFailedTest($test, $expRC, $actRC);
                }
                if (!$settings->noclean)
                {
                    unlink(realpath($test.".intOut"));
                }
            }
            else
            {// error return code - only care about return code
                $command = "php8.1 $settings->parseScript < $test.src | python3.8 $settings->intScript --input=$test.in";
                exec($command, $output, $actRC); 
                $this->checkOnlyRetCodes($expRC, $actRC, $test);                    
            }
        }
    }

        /**
     * Performs parser tests.
     * @param $config - object containing current testing configurantion
     * @param list $testFiles - list of files containig tests
     */
    private function parserTest($settings, $testFiles)
    {
        foreach($testFiles as $test)
        {   
            $expRC = file_get_contents($test . ".rc");
            if($expRC === "0")
            { // succes return code - compare outputs
                $command = "php8.1 $settings->parseScript < $test.src > $test.parseOut";
                exec($command, $output, $actRC); 

                if($expRC == $actRC)
                { // identical return codes - compare outputs
                    $command = "java -jar $settings->jexampath/$settings->jexamxml $test.parseOut $test.out $settings->jexampath/$settings->options";
                    exec($command, $output, $diffRC); 
                    $this->checkDiffRetCode($diffRC, $test);
                }
                else
                {  // actual and expected return code differ
                    $this->newFailedTest($test, $expRC, $actRC);
                }

                if (!$settings->noclean)
                { // remove temponry test files
                    unlink(realpath($test.".parseOut"));
                }
            }
            else
            {// error return code - only care about return code
                $command = "php8.1 $settings->parseScript < $test.src";
                exec($command, $output, $actRC); 
                $this->checkOnlyRetCodes($expRC, $actRC, $test);                    
            }
        }
    }
    
    /**
     * Performs interpreter tests.
     * @param $config - object containing current testing configurantion
     * @param list $testFiles - list of files containig tests
     */
    private function interpretTest($settings, $testFiles)
    {
        foreach($testFiles as $test)
        {   
            $expRC = file_get_contents($test . ".rc");
            if($expRC === "0")
            { // succes return code - compare outputs
                $command = "python3.8 $settings->intScript --input=$test.in <$test.src >$test.intOut";
                exec($command, $output, $actRC);

                if($expRC == $actRC)
                { // identical return codes - compare outputs
                    $command = "diff $test.intOut $test.out";
                    exec($command, $output, $diffRC); 

                    $this->checkDiffRetCode($diffRC, $test);
                }
                else
                {  // different return codes
                    $this->newFailedTest($test, $expRC, $actRC);
                }
                if (!$settings->noclean)
                {
                    unlink(realpath($test.".intOut"));
                }
            }
            else
            {// error return code - only care about return code
                $command = "python3.8 $settings->intScript --input=$test.in <$test.src";
                exec($command, $output, $actRC); 
                $this->checkOnlyRetCodes($expRC, $actRC, $test);                    
            }
        }
    }
    
    /**
     * Checks test results and creates new test result.
     * @param $expRC - expected return code
     * @param $actRC - actual return code
     * @param $test - name of test 
     */
    private function checkOnlyRetCodes($expRC, $actRC, $test)
    {
        if($expRC == $actRC)
        { 
            $this->newPassedTest($test);                
        }
        else
        {
            $this->newFailedTest($test, $expRC, $actRC);
        }   
    }

        
    /**
     * Checks test results and creates new test result.
     * @param $diffRC - return value of previous diff execuion
     * @param $test - name of test 
     */
    private function checkDiffRetCode($diffRC, $test)
    {
        if ($diffRC == 0)
        { // identical outputs
            $this->newPassedTest($test);
        }
        else
        { // different outputs
            $this->newFailedTest($test);
        }
    }

    /**
     * Creates new test result that has passed.
     * @param $filePath - filepath to the test
     */
    private function newPassedTest($filePath)
    {
        $this->testResults[] = new TestResult($this->counter++, $filePath, True);
        $this->passedCount++;               
    }

    /**
     * Creates new test result that has failed.
     * @param $filePath -  filepath to the test
     * @param $expRc - expected return code (in case of different return codes)
     * @param $actRc - actual return code (in case of different return codes)
     */
    private function newFailedTest($filePath, $expRC=NULL, $actRC=NULL)
    {
        $this->testResults[] = new TestResult($this->counter++, $filePath, False, $expRC, $actRC);
        $this->failedCount++;    
    }
}


?>