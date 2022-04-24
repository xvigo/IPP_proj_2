all: both int-only parse-only

both:
	php test.php --parse-script=../parse/odevzdani/xgottw07/parse.php --int-script=interpret.py --directory=../ipp-2022-tests/both --recursive > ./results/test-both.html

int-only:
	php test.php --int-script=./interpret.py --directory=../ipp-2022-tests/interpret-only --recursive  --int-only > ./results/test-int.html

parse-only:
	php test.php --parse-script=../parse/odevzdani/xgottw07/parse.php --directory=../ipp-2022-tests/parse-only --recursive --parse-only > ./results/test-parse.html

error:
	php test.php --parse-only --interpret-only --recursive

