<?php

/**
 * @package IPP project 2022 - test.php
 * @author Vilem Gottwald
 */

 /**
  * Class with return values constants.
  */
final class ReturnValues
{
    // general
    public const SUCCESS = 0; // no error
    public const PARAMETER_ERR = 10; // missing script parameter or invalid combination of parameters
    public const INPUT_FILE_ERR = 11; // error while opening input file
    public const OUTPUT_FILE_ERR = 12; // error while opening output file
	public const INTERNAL_ERR = 99; // internal error (e.g. memmory error)

    // test
    public const PATH_ERR = 41; // directory or file given in parameter doens't exist or ins't accesible 

}
?>
