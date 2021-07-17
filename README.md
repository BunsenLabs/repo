## repo - APT repository management tool

This is `repo`, a command line tool for managing APT repository configuration. It exposes
functionality implemented by Debian's `python-apt` library, and adds some own things.

`repo` does not micro-manage your sources.list entries. It works
according to the priciniple: given such and such an entry, **ensure that
it exists as specified**. That means, when you want to *add* a
sources.list entry, and a 'disabled' old entry close to the new one
already exists, the old entry will be re-used and modified.
