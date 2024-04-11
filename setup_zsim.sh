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

# Now, I needed to run "echo 0 > /proc/sys/kernel/yama/ptrace_scope", but
# could only do it using sudo -i (may be different for others)
# This can be done like this:
# sudo -i
# sudo echo 0 > /proc/sys/kernel/yama/ptrace_scope

# Maybe this will work
echo "0"|sudo tee /proc/sys/kernel/yama/ptrace_scope

git clone https://github.com/abe-f/zsim.git

# Build
cd zsim
scons -j16

# Verify build with test program
./build/opt/zsim tests/simple.cfg

mkdir cs533
cd cs533

# Copy large.cfg from computer into cs533 folder

mkdir benchmarks
cd benchmarks

git clone https://github.com/abe-f/graphBIG.git

#graphBIG
# add this to make files with flags:
# -Wno-format-truncation
# put brackets around for loops to fix errors

cd graphBIG/dataset
mkdir large
cd large
# copy gen_data.py into folder
python3 gen_data.py

cd ../..

cd benchmark
make clean all
#cd *page*
#make

cd ../../..

./build/opt/zsim cs533/large.cfg