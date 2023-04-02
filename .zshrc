##### SET SCHRODINGER ENVIRONMENT VARIABLES #####
BASE_FOLDER=~/builds
export SCHRODINGER_LIB=$BASE_FOLDER/software/lib


### Parse git branch in terminal.
parse_git_branch() {
 git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

if [[ $OSTYPE == "darwin"* ]] 
then
  setopt PROMPT_SUBST ; PS1='[%n@%m %c $(parse_git_branch) ]\$ '
else
  PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[01;31m\]$(parse_git_branch)\[\033[00m\]\$ '
fi

### Alias
alias buildinger='$SCHRODINGER_SRC/mmshare/build_tools/buildinger.sh'
alias pmk='$SCHRODINGER_SRC/mmshare/premake $PREMAKE_OPTION'
alias wb='waf configure build install --build=$BUILD_TYPE'
alias wafclean='waf configure clean'
alias waftest='waf configure build install --test'
alias waflist='waf configure list'
alias myclang='clang-format --style=file -i '
alias yapf='yapf -i '
alias mae='$SCHRODINGER/maestro $CONSOLE_OPTION'
alias maes='cd $SCHRODINGER_SRC/maestro-src'
alias mms='cd $SCHRODINGER_SRC/mmshare'
alias mat='$SCHRODINGER/materials $CONSOLE_OPTION'
alias mrun='$SCHRODINGER/run'
alias ff='$SCHRODINGER_SRC/mmshare/build_tools/cpp_format.sh'
alias mmstest='$SCHRODINGER_SRC/mmshare/build_tools/run_maestro_tests.sh'
alias pytest='$SCHRODINGER/utilities/py.test'
alias maetest='$SCHRODINGER/utilities/py.test $SCHRODINGER/maestro-v*/'
alias buildinger='$SCHRODINGER_SRC/mmshare/build_tools/buildinger.sh'
alias sshbolt='ssh $USER@boltsub3.schrodinger.com'
alias post='rbt post --tracking-branch=$WORKING_BRANCH'
alias land='rbt land --dest=$WORKING_BRANCH --edit --squash'
alias sshlinux='ssh 172.22.46.74'

ticket()
{
  current_branch=$(parse_git_branch)
  current_branch=${current_branch:1:-1}
  if [[ "$current_branch" == "$WORKING_BRANCH" ]]; then
    echo "You are on $WORKING_BRANCH branch. Please checkout to your ticket branch."
    return
  fi
  open "https://jira.schrodinger.com/browse/$current_branch"
}

print_envs(){
    echo "WORKING_BRANCH = $WORKING_BRANCH"
    echo "RELEASE = $RELEASE"
    echo "BUILD_TYPE = $BUILD_TYPE"
    echo "SCHRODINGER_SRC = $SCHRODINGER_SRC"
    echo "SCHRODINGER = $SCHRODINGER"
    echo "SCHRODINGER_LIB = $SCHRODINGER_LIB"
}