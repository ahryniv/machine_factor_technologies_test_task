import pkg_resources


try:
    __version__ = pkg_resources.get_distribution('parquet_web_socket').version

except pkg_resources.DistributionNotFound:
    __version__ = 'unknown'
