export $(egrep -v '^#' ../.env | xargs)
python -c "import sys, pkgutil; sys.exit(0 if pkgutil.find_loader('pymongo') else 1)" || ( \
    curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && \
    sudo python get-pip.py && \
    sudo pip install "pymongo==3.5.1" )