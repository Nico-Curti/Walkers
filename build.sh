#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
  export CC="/usr/local/bin/gcc"
  export CXX="/usr/local/bin/g++"
else
  export CC="/usr/bin/gcc-8"
  export CXX="/usr/bin/g++-8"
fi

#rm -rf build
mkdir -p build
cd build

##sudo apt-get install ninja-build
#cmake -G "Ninja" "-DCMAKE_BUILD_TYPE=Release" ..
cmake -DOMP=OFF ..
make -j
cmake --build . --target install
cd ..
