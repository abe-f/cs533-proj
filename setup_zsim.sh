sudo apt-get update -y

# Install pin into pin folder, export env. variable
wget https://software.intel.com/sites/landingpage/pintool/downloads/pin-2.14-71313-gcc.4.4.7-linux.tar.gz
tar -xvf pin*.tar.gz
rm -rf pin*.tar.gz
mv pin* pin
export PINPATH=$(pwd)/pin

sudo apt-get install -y libconfig++-dev
#sudo apt-get install -y libconfig-dev # might be needed
sudo apt-get install -y libhdf5-dev
export HDF5PATH=/usr/lib/x86_64-linux-gnu/hdf5/serial

sudo apt-get install -y scons
sudo apt-get install -y libelf-dev

# idk what this does but i hope it's not bad
echo "0"|sudo tee /proc/sys/kernel/yama/ptrace_scope

git clone https://github.com/abe-f/zsim.git

# Build zsim
cd zsim
scons -j16

# Verify build with test program
./build/opt/zsim tests/simple.cfg

cd ..
mkdir benchmarks
cd benchmarks

# Clone graphBIG benchmark suite
git clone https://github.com/abe-f/graphBIG.git

# Run script that will download large twitter graph data
cd graphBIG/dataset/large
python3 gen_data.py

# Build graphBIG
cd ../..
cd benchmark
make clean all

# Install python libraries
sudo apt install python3-pip -y
pip install h5py

cd ../../../../..

#./build/opt/zsim cs533/large.cfg

#cd cs533
#python3 analyze_data.py