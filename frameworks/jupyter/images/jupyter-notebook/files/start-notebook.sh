#!/usr/bin/env bash

set -x

if getent passwd $NB_USER; then
	echo "User $NB_USER already exists"
else
	useradd -m -s /bin/bash -N $NB_USER
fi

mkdir /home/$NB_USER/work
mkdir /home/$NB_USER/.jupyter
mkdir /home/$NB_USER/.local
mkdir -p /home/$NB_USER/.ipython/profile_default/startup/

cp -a /home/nbuser/.jupyter /home/$NB_USER
cp -a /home/nbuser/.local /home/$NB_USER
cp -a /home/nbuser/.ipython /home/$NB_USER

chown -R $NB_USER /home/$NB_USER/work /home/$NB_USER/.jupyter /home/$NB_USER/.local /home/$NB_USER/.ipython /mnt/workspace

cd /mnt/workspace

su $NB_USER -c "env PATH=/opt/conda/bin:$PATH R -e \"IRkernel::installspec()\""
su $NB_USER -c "env PATH=/opt/conda/bin:$PATH ipcluster nbextension enable"

exec su $NB_USER -c "env PATH=$PATH jupyter notebook $*"

exit

# Handle special flags if we're root
if [ $UID == 0 ] ; then
    # Change UID of NB_USER to NB_UID if it does not match
    if [ "$NB_UID" != $(id -u $NB_USER) ] ; then
        usermod -u $NB_UID $NB_USER
        chown -R $NB_UID $CONDA_DIR
    fi

    # Enable sudo if requested
    if [ ! -z "$GRANT_SUDO" ]; then
        echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook
    fi

    # Start the notebook server
    exec su $NB_USER -c "env PATH=$PATH jupyter notebook $*"
else
    # Otherwise just exec the notebook
    exec jupyter notebook $*
fi

