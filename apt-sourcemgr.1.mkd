% apt-sourcemgr(1) User Manual
% Jens John <dev@2ion.de>
% Version 0.1

# NAME

apt-sourcemgr - Tool for managing local APT sources.list configuration

# SYNOPSIS

apt-sourcemgr [`-h` | `--help`] [`OPTION`]... [`--`] `VERB`

# DESCRIPTION

**apt-sourcemgr** is a command line interface for managing the of the
sources.list configuration of the local system as used by the Debian APT
package management tools. Its working principle is to first *select* a
set of source entries using criterea received via option arguments and
then perform an action given by **VERB** on it.

# ACTIONS

  * **add**: Ensure that an entry matching the given criteria is present and
    enabled.
  * **apply-template**: A special case of the **add** action. A
    python-apt distribution template is used as a source of entries, and
    all entries matching the specification are added to the system
    configuration.
  * **disable**: Disable existing entries matching the given criteria. An
    entry is said to be disabled when its line in the configuration
    starts with a `#` character.
  * **enable**: Enable entries matching the given criteria. An entry
    is said to be enabled when it isn't commented out in the
    configuration file.
  * **find**: Find existing entries matching the filter specification
    and print them to standard output.
  * **remove**: Remove entries matching the given criteria.

# OPTIONS

Options affect how actions are executed or may change how other options
are interpreted. The `-h`, `--help` option is special; it prints a help text
and immediately ends the program.

# SEE ALSO

**sources.list**(5).
