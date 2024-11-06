#! bash oh-my-bash.module
# This is combination of works from two different people which I combined for my requirement.
# Original PS1 was from reddit user /u/Allevil669 which I found in thread: https://www.reddit.com/r/linux/comments/1z33lj/linux_users_whats_your_favourite_bash_prompt/
# I used that PS1 to the bash-it theme 'morris', and customized it to my liking. All credits to /u/Allevil669 and morris.
#
# prompt theming

_omb_module_require plugin:battery

BOLD="\[\033[1m\]"
RED="\[\033[91m\]"
GREEN="\[\033[32m\]"
YELLOW="\[\033[93m\]"
BLUE="\[\033[94m\]"
PURPLE="\[\033[95m\]"
CYAN="\[\033[96m\]"
WHITE="\[\033[37m\]"
NORMAL="\[\033[0m\]"

function _omb_theme_PROMPT_COMMAND() {
  local status=$?

  local BC=$(battery_percentage)
  [[ $BC == no && $BC == -1 ]] && BC=
  BC=${BC:+${WHITE}─${YELLOW}[$BC%]}

  local python_venv
  _omb_prompt_get_python_venv

  PS1="\n${WHITE}┌─${BOLD}${RED}[\u@\h]${WHITE}─${PURPLE}(\w)${BLUE}$(scm_prompt_info)$python_venv\n${WHITE}└─${GREEN}[\A]$BC${WHITE}─${CYAN}[$]${NORMAL} "
}

# scm theming
SCM_THEME_PROMPT_DIRTY=" ${_omb_prompt_bright_red}✗${BLUE}"
SCM_THEME_PROMPT_CLEAN=" ${GREEN}✓${BLUE}"
SCM_THEME_PROMPT_PREFIX="${WHITE}─("
SCM_THEME_PROMPT_SUFFIX="${WHITE})"

OMB_PROMPT_SHOW_PYTHON_VENV=${OMB_PROMPT_SHOW_PYTHON_VENV:-true}
OMB_PROMPT_VIRTUALENV_FORMAT="${WHITE}(%s)${NORMAL}"
OMB_PROMPT_CONDAENV_FORMAT="${WHITE}(%s)${NORMAL}"

_omb_util_add_prompt_command _omb_theme_PROMPT_COMMAND
