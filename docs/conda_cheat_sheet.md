# Create a new environment
conda create --name envname

# Activate an environment
conda activate envname

# Deactivate the current environment
conda deactivate

# List all environments
conda info --envs

# List installed packages
conda list

# Search for a package
conda search packagename

# Install a package
conda install packagename

# Install a specific version of a package
conda install packagename=1.2.3

# Install from a specific channel
conda install -c channelname packagename

# Remove a package
conda remove packagename

# Update all packages in the current environment
conda update --all

# Export the environment to a YAML file
conda env export > environment.yml

# Create an environment from a YAML file
conda env create -f environment.yml
