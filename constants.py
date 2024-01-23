import os

# Are we developing locally?
# In the deployment docker file, we set the environment variable DJ_LOCAL to False
LOCAL: bool = os.environ.get('DJ_LOCAL', 'True') == 'True'


class WrappedConstants:
    DOCKER_VOLUME = 'persist_vol'
    pass


DOCKER_VOLUME = f'/{WrappedConstants.DOCKER_VOLUME}' if not LOCAL else WrappedConstants.DOCKER_VOLUME
