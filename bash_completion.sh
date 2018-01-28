#!/bin/bash
_apt_sourcemgr () {
  local cur=${COMP_WORDS[COMP_CWORD]}
  local prev=${COMP_WORDS[COMP_CWORD-1]}
  local dashed="-F --file  -D --disabled  -E --enabled  -I --invalid  -a --architecture  -c --component  -d --distribution  -f --fuzzy  -r --regex  -t --type  -u --uri  -s --simulate  -T --template"
  local verbs="add remove enable disable apply-template"
  if [[ -z "$cur"  ]]; then
    COMPREPLY=($(compgen -W "$dashed $verbs" -- "$cur"))
    return
  elif [[ $cur =~ ^- ]]; then
    COMPREPLY=($(compgen -W "$dashed" -- "$cur"))
    return
  else
    COMPREPLY=($(compgen -W "$verbs" -- "$cur"))
    return
  fi
}
complete -o default -F _apt_sourcemgr apt-sourcemgr
