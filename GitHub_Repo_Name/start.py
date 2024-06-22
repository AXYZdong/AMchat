import os

base_path = './AMChat_internlm2-math-plus-7b_Hong'
# download repo to the base_path directory using git
os.system('apt install git')
os.system('apt install git-lfs')
os.system(f'git clone https://code.openxlab.org.cn/chg0901/AMChat_internlm2-math-plus-7b_Hong.git {base_path}')
os.system(f'cd {base_path} && git lfs pull')