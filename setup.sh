echo "Setting up .dotfiles"

files=[".vimrc",".zshrc"]

function setup_files(){

base_location = $1

for file in $files:
    ln -s $1/$file ~/$file


cat $base_location/.gitconfig >> ~/.gitconfig
}
