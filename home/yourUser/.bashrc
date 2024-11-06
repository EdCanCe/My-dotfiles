case $- in
  *i*) ;;
    *) return;;
esac

export OSH='/home/yourUser/.oh-my-bash'

OSH_THEME="kitsune"

OMB_USE_SUDO=true

completions=(
  git
  composer
  ssh
)

aliases=(
  general
)

plugins=(
  git
  bashmarks
)

source "$OSH"/oh-my-bash.sh

alias bashconfig="nvim ~/.bashrc"
alias ohmybash="nvim ~/.oh-my-bash"
alias code="flatpak run com.visualstudio.code"

./Scripts/start.sh
