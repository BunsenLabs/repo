% apt-sourcemgr(1) User Manual
% Jens John <dev@2ion.de>
% Version 0.1

# NAME

apt-sourcemgr - Tool for managing local APT sources.list configuration

# SYNOPSIS

apt-sourcemgr [`-h` | `--help`] `ACTION` [`OPTION`]...

# DESCRIPTION

**apt-sourcemgr** is a command line interface for managing the of the
sources.list configuration of the local system as used by the Debian APT
package management tools. Its working principle is to first *select* a
set of source entries using criterea received via option arguments and
then perform an action given by **ACTION** on it.

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


### -h, --help

Show this help message and exit.

### -F FILE, --file FILE 

Path to the .list file to store the entry in. Works only with the `add`
verb. Note that if a similar entry already exists (for example when just
adding a component), or if the entry is present but disabled), the
existing entry will be reused, modified and the file argument will be
ignored. (default: None)

### -D, --disabled

Matches disabled (commented-out) entries. (default: None)

### -E, --enabled

Matches enabled entries. (default: None)

### -I, --invalid

Matches invalid entries. (default: False)

### -a ARCHITECTURE, --architecture ARCHITECTURE

Matches entries with the given architecture(s).  May be specified
multiple times. (default: None)

### -c COMPONENT, --component COMPONENT

Matches entries with the given component(s). May be specified multiple
times. (default: None)

### -d DISTRIBUTION, --distribution DISTRIBUTION

Matches the given distribution. (default: None)

### -f, --fuzzy

Normally, whenever a list-based filter parameter is being evaluated,
entries only match if they fulfill the specification completely. For
example, when filtering using `--component main`, entries which
possess the component `main` but also `contrib` will not match. By
setting this flag, entries will match if *any* of the command line
filter paramters will match.  Applies only to: --architecture,
--component.  (default: False)

### -r, --regex

--uri, --distribution and --component will now be evaluated as
case-insensitive regular expressions against the entry. When used with
`apply-template`, the behaviour of --component is different. Only the
first occurrence of --component will be taken as the regex and only
components matching that regex will be included in the final entry.
(default: False)

### -t {deb,deb-src}, --type {deb,deb-src}

DEB source type. (default: None)

### -u URI, --uri URI

Source URI. (default: None)

### -s, --simulate

Do not save any changes, and log all changed source entries to stdout.
(default: False)

### -T TEMPLATE, --template TEMPLATE

Derive all specifications from the given pyton-apt template. Only used
by the apply-template action.  (default: None)

# SEE ALSO

**sources.list**(5).
