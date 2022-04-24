<?php

/**
 * @package IPP project 2022 - test.php
 * @author Vilem Gottwald
 */

 /**
 * Class that stores HTML snippets used for generating test results HTML.
 */
final class HTML
{
    static $head = <<<EOD
    <!DOCTYPE html>
    <html lang="cs">
    <head>
    <meta charset="UTF-8">
    <style>

    .result {
        color: black;
        margin-left: 15%;
        margin-right: 15%;
        margin-bottom: 20px;
        padding:0.01em 16px;
        display: grid;
        grid-template-columns: 60px auto auto;
        align-items:center;
    }

    .failed {
        border-left:10px solid #c71414 !important;
        background-color: rgb(255, 231, 231);
    }

    .passed {
        border-left:10px solid #04aa6d !important;
        background-color: rgb(231, 253, 231);
    }

    .result .order {
        font-size: 130%;
    }

    .result .type {
        text-align: right;
        font-size: 200%;
        margin-left: 25px;
    }

    .failed .type {
        font-weight: 900;
    }

    .flex-container {
        display: flex;
        justify-content: space-between;
    }

    .flex-container > div {
        background-color: #f1f1f1;
        margin: 10px;
        padding: 20px;
        flex-wrap: wrap;
        justify-content: space-between;
    }

    .flex-container .config {
        width: 35%;
        padding-top: 0px;
        margin-left: 20px;
        margin-right: 0px;
    }

    .flex-container .summary {
        width: 55%;
        padding-top: 0px;
        display: grid;
        grid-template-areas: 
        'header header' 
        'left right';
        align-items:center;
        justify-content: stretch;
        margin-right: 20px;
        margin-left: 0px;
    }

    .error {
        color: red;
        font-weight: bold;
    }

    ul {
        list-style-type: "- ";
    }

    .textCentered {
        text-align: center;
    }

    .pageHeader {
        background-color: rgb(158, 158, 158);
        padding: 10px;
        margin: -10px;
        margin-bottom: 5px;
    }

    .header {
        grid-area: header;
    }

    .percentage {
        font-size: 400%;
        font-weight: 600;
        grid-area: left;
        text-align: center;    
    }

    .counts {
    grid-area: right;
    line-height: 1.5 ;
    }

    </style>

    <title>IPP22 Výsledky testů</title>
    </head>\n
    EOD;

    static $header = <<<EOD
    <body>

    <h1 class="pageHeader">IPP 2022 - výsledky testů</h1>\n
    EOD;

    static $configStart = <<<EOD
    <div class="flex-container">
        <div class="config">
            <h3>Konfigurace</h3>
            <ul>\n
    EOD;

    static $configEnd = <<<EOD
    </ul>
    </div>\n
    EOD;

    static $summaryStart = <<<EOD
    <div class="summary">
    <h3 class="header">Souhrn</h3>\n
    EOD;


    static $summaryEnd = <<<EOD
    </ul>
    </div>
    </div>\n
    EOD;

    static $resultsHeader = <<<EOD
    <br><br>
    <h2 class="textCentered"> Výsledky jednotlivých testů</h2>
    <br>\n
    EOD;

    static $pageEnd = <<<EOD
    </body>
    </html>\n
    EOD;
}
?>