export PATH=/opt/homebrew/bin:$PATH
alias myste='cd /Users/hojunhwang/Desktop/SK_Family_AI/projects/mysite;source /Users/hojunhwang/Desktop/SK_Family_AI/venvs/mysite/bin/activate'

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/hojunhwang/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/hojunhwang/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/Users/hojunhwang/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/hojunhwang/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

