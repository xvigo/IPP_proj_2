<?php

/**
 * @package IPP project 2022 - test.php
 * @author Vilem Gottwald
 */

require_once(__DIR__. "/test-lib/CLA_GetSettings.php");
require_once(__DIR__. "/test-lib/Tester.php");
require_once(__DIR__. "/test-lib/TestFilesManager.php");

$settings = new CLA_GetSettings();

$testFiles = TestFilesManager::getTestsFromDir($settings->directory, $settings->recursive);
TestFilesManager::generateMissingTestFiles($testFiles);

$tester = new Tester();
$tester->test($settings, $testFiles);
$tester->printTestsHtml($settings);

?>