## [0.5.0] - 2021-07-29

* cp2kparse: parse SIRIUS warnings & errors
* cp2kparse: parse DOI for automated citation generation
* bandstructure_parse: add API (based on cp2k_bs2csv script)
* cp2k_bs2csv: move to cli and use click (adds output dir option)

## [0.4.0] - 2021-07-19

* cp2kparse/api: can now parse forces
* cp2kparse: gained a highlight mode to show what gets matched
* cp2kparse: moved to click for providing the CLI to improve UX
* cp2kparse/api: fix bug with parsing line continued kv
* api: introduced BlockMatch to provide more info about the match (like the char span)
* cp2k_bs2csv: generate files in CWD rather than in source dir

## [0.3.1] - 2020-09-09

* cp2k_pdos: add support for list-of-atoms output

## [0.3.0] - 2020-09-09

* add cp2k_pdos tool
* reorganize scripts/ dir

## [0.2.0] - 2020-05-05

* add cp2k_bs2csv with support for CP2K v8+ and an API
* add xyz_restart_cleaner

## [0.1.4] - 2020-04-03

* updated project urls

## [0.1.3] - 2020-02-25

* more tests
* functionality to 'sanitize' key names

## [0.1.2] - 2020-02-19

* parse more key-value sections and divide into subsections
* support yaml for output
* allow pulling only specific keys

## [0.1.1] - 2020-02-19

(release testing)

## [0.1.0] - 2020-02-19

Initial release
