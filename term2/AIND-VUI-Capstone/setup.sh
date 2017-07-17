git config --global user.email "chen1474@purdue.edu"
git config --global user.name "Gelei Chen"
export PATH=~/anaconda3/bin:$PATH
conda create --name aind-vui python=3.5 numpy
source activate aind-vui
pip install tensorflow-gpu==1.1.0
pip install -r requirements.txt
KERAS_BACKEND=tensorflow python -c "from keras import backend"
sudo apt-get install libav-tools
jupyter notebook --ip=0.0.0.0 --no-browser

