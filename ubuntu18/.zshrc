# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="refined"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  zsh-autosuggestions
  git
  ubuntu
)

source $ZSH/oh-my-zsh.sh

#=============================================================================#
# appending anaconda envrionment
pathappend() {
  if ! echo $PATH | /bin/egrep -q "(^|:)$1($|:)" ; then
     if [ "$2" = "after" ] ; then
        PATH=$PATH:$1
     else
        PATH=$1:$PATH
     fi
  fi
}
# removing anaconda evnrionment
pathremove() {
  # Delete path by parts so we can never accidentally remove sub paths
  PATH=${PATH//":$1:"/":"} # delete any instances in the middle
  PATH=${PATH/#"$1:"/} # delete any instance at the beginning
  PATH=${PATH/%":$1"/} # delete any instance in the at the end
}

# arg1 is the path, arg2 is where to put it
pythonpathappend() {
  if ! echo $PYTHONPATH | /bin/egrep -q "(^|:)$1($|:)" ; then
     if [ "$2" = "after" ] ; then
        PYTHONPATH=$PYTHONPATH:$1
     else
        PYTHONPATH=$1:$PYTHONPATH
     fi
     export PYTHONPATH
  fi
}

pythonpathremove() {
  # Delete path by parts so we can never accidentally remove sub paths
  PYTHONPATH=${PYTHONPATH//":$1:"/":"} # delete any instances in the middle
  PYTHONPATH=${PYTHONPATH/#"$1:"/} # delete any instance at the beginning
  PYTHONPATH=${PYTHONPATH/%":$1"/} # delete any instance in the at the end
}

# better way to add path since this checks path existance
addToPATH() {
  case ":$PATH:" in
    *":$1:"*) :;; # already there
    *) PATH="$1:$PATH";; # or PATH="$PATH:$1"
  esac
}

# alias acond='pathappend $HOME/anaconda3/bin'
# alias rcond='pathremove $HOME/anaconda3/bin'

# Virtual Environment Wrapper
# source /usr/local/bin/virtualenvwrapper.sh

# anaconda python path
# acond

pythonpathappend /usr/local/lib
# export PYTHONPATH=$PYTHONPATH:/usr/local/lib

#=============================================================================#
# alias:
alias nvwatch='watch -n 2 nvidia-smi'
alias chrome='google-chrome'

# Type Alias:
alias zshconfig="atom ~/.zshrc"
alias vzsh="vim ~/.zshrc"
alias szsh="source ~/.zshrc"

# ls, the common ones I use a lot shortened for rapid fire usage
alias l='ls -lFh'     #size,show type,human readable
alias la='ls -lAFh'   #long list,show almost all,show type,human readable
alias lr='ls -tRFh'   #sorted by date,recursive,show type,human readable
alias lt='ls -ltFh'   #long list,sorted by date,show type,human readable
alias ll='ls -l'      #long list

# I'll start by adding the most essential.
alias o="nautilus"
alias x="exit"
alias g="git"
alias gs='git status'
alias gd='git diff'
alias g-='git checkout -'
alias serve='python -m http.server 8000'
alias cppcompile='c++ -std=c++11 -stdlib=libc++'
alias tgz='tar -zxvf'
alias rm='rm -i'
alias hg='history | grep'


# copy and paste
alias pbcopy='xclip -selection clipboard'
alias pbpaste='xclip -selection clipboard -o'


#=============================================================================#

# Options:
setopt no_share_history
HISTFILE=~/private/.zsh_history
HISTSIZE=10000000
SAVEHIST=10000000
function history-all() { history -E 1 }  # print out all history 

#=============================================================================#

