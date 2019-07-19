import os
from abc import ABCMeta
import os.path

__all__ = [
  'FS', 'File', 'IMAGE_TYPES',
]

################################################################################################
# +--------------------------------------------------------------------------------------------+
# | FS snd File: File System.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class FS:
    # Project name & absolute directory.
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    APP_NAME = os.path.basename(PROJECT_DIR)

    IMAGEQ_DIR = os.path.join(PROJECT_DIR, "ImageQ")
    SEARCH_DIR = os.path.join(IMAGEQ_DIR, "search")
    CACHE_DIR = os.path.join(IMAGEQ_DIR, "cache")

    SEARCH_CACHE = os.path.join(CACHE_DIR, "images")
    LOG_DIR = os.path.join(CACHE_DIR, "logs")
    MODEL_DIR = os.path.join(CACHE_DIR, "models")


class File(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def make_dirs(path: str, verbose: int = 0):
        """Create Directory if it doesn't exist.

        Args:
            path (str): Directory/directories to be created.
            verbose (bool, optional): Defaults to 0. 0 turns of logging, /
                while 1 gives feedback on creation of director(y|ies).

        Example:
            >>> path = os.path.join("path/to", "be/created/")
            >>> File.make_dirs(path, verbose=1)
            INFO  |  "path/to/be/created/" has been created.

        """

        # if director(y|ies) doesn't already exist.
        if not os.path.isdir(path):
            # Create director(y|ies).
            os.makedirs(path)

            # if verbose:
            #     # Feedback based on verbosity.
            #     Log.info('"{}" has been created.'.format(os.path.relpath(path)))

    @staticmethod
    def get_dirs(path: str, exclude= None, optimize: bool = False):
        """Retrieve all directories in a given path.

        Args:
            path (str): Base directory of directories to retrieve.
            exclude (Iterable[str], optional): Defaults to None. List of paths to /
                remove from results
            optimize (bool, optional): Defaults to False. Return an generator object, /
                to prevent loading all directories in memory, otherwise: return results /
                as a normal list

        Raises:
            FileNotFoundError: `path` was not found

        Returns:
            Union[Generator[str], List[str]]: Generator expression if optimization is turned on, /
                otherwise list of directories in given path

        """
        # Return only list of directories.
        return File.listdir(path, exclude=exclude, dirs_only=True, optimize=optimize)

    @staticmethod
    def get_files(path: str, exclude= None, optimize: bool = False):
        """Retrieve all files in a given path.

        Args:
            path (str): Base directory of files to retrieve.
            exclude (Iterable[str], optional): Defaults to None. List of paths to /
                remove from results.
            optimize (bool, optional): Defaults to False. Return an generator object, /
                to prevent loading all directories in memory, otherwise: return results /
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[str], List[str]]: Generator expression if optimization is turned on, /
                otherwise list of files in given path.

        """
        # Return only list of directories.
        return File.listdir(path, exclude=exclude, files_only=True, optimize=optimize)

    @staticmethod
    def listdir(path: str, exclude= None,
                dirs_only: bool = False, files_only: bool = False,
                optimize: bool = False):
        r"""Retrieve files/directories in a given path.

        Args:
            path (str): Base directory of path to retrieve.
            exclude (Iterable[str], optional): Defaults to None. List of paths to /
                remove from results.
            dirs_only (bool, optional): Defaults to False. Return only directories in `path`.
            files_only (bool, optional): Defaults to False. Return only files in `path`.
            optimize (bool, optional): Defaults to False. Return an generator object, /
                to prevent loading all directories in memory, otherwise: return results /
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[str], List[str]]: Generator expression if optimization is turned on, /
                otherwise list of directories in given path.

        """
        if not os.path.isdir(path):
            raise FileNotFoundError('"{}" was not found!'.format(path))

        # Get all files in `path`.
        if files_only:
            paths = (os.path.join(path, p) for p in os.listdir(path)
                     if os.path.isfile(os.path.join(path, p)))
        else:
            # Get all directories in `path`.
            if dirs_only:
                paths = (os.path.join(path, p) for p in os.listdir(path)
                         if os.path.isdir(os.path.join(path, p)))
            else:
                # Get both files and directories.
                paths = (os.path.join(path, p) for p in os.listdir(path))

        # Exclude paths from results.
        if exclude is not None:
            # Remove excluded paths.
            paths = filter(lambda p: os.path.basename(p) not in exclude, paths)

        # Convert generator expression to list.
        if not optimize:
            paths = list(paths)

        return paths

# image constants
IMAGE_TYPES = {
    'image/png': "png",
    'image/jpeg': "jpeg",
    'image/jpg': "jpg",
}

# Search string Constants

SEARCH_QUERY = {
    "Google": 'https://www.google.com/search?q={}&start={}',
    "Yahoo": 'https://search.yahoo.com/search?p={}&b={}',
    "Bing": 'https://www.bing.com/search?q={}&count=10&offset=0&first={}',

}

HEADERS = {
            "Cache-Control": 'no-cache',
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }