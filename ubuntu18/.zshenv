# Must have Path exports: 
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export PATH=/usr/local/cuda/bin:$PATH
export CPATH=/usr/local/cuda/include:$CPATH

if [ -z "$SINGULARITY_CONTAINER" ]; then
  # pyenv:
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH=${PYENV_ROOT}/bin:$PATH
  if command -v pyenv 1>/dev/null 2>&1; then
    eval "$(pyenv init -)"
    # eval "$(pyenv virtualenv-init -)"
  fi
else
    echo "running a singularity container!!!!!"
fi

# modmap
{
  cmd=`xmodmap -pke | grep -w Caps_Lock`
  if [ $? -eq 0 ]; then
    xmodmap .Xmodmap
  fi
} 2> /dev/null
