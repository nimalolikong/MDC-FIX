#!/bin/sh

git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
grep -q '^plugins=' ~/.zshrc && \
sed -i.bak 's/^plugins=([^)]*)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting z)/' ~/.zshrc || \
echo 'plugins=(git zsh-autosuggestions zsh-syntax-highlighting z)' >> ~/.zshrc
echo 'cd ~ && sudo cp -r -n /home/coder/resource/output/* /home/coder/savepath && rm -rf /home/coder/resource/output' >> ~/.mv_to_lol.sh