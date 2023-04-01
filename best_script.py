import os
import subprocess
import contextlib
import glob

SCHRODINGER = os.getenv("SCHRODINGER")
SCHRODINGER_SRC = os.getenv("SCHRODINGER_SRC")
MAESTRO_SRC = "maestro-src"
MMSHARE = "mmshare"
REPOS = [MMSHARE, MAESTRO_SRC]
CLANG_CMD = ["clang-format", "--style=file", "-i"]
YAPF_CMD = ["yapf", "-i"]
FLAKE_CMD = ["flake8"]
BUILD_TYPE = "debug"  # or "optimized"
WAFBUILD = f"waf configure build install --build={BUILD_TYPE}"
MMSHARE_SRC_PATH = os.path.join(SCHRODINGER_SRC, MMSHARE)
MAESTRO_SRC_PATH = os.path.join(SCHRODINGER_SRC, MAESTRO_SRC)


@contextlib.contextmanager
def cd_dir(new_dir):
    old_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)


def get_mmshare_build_dir():
    mmshare_build_exp = os.path.join(SCHRODINGER, "mmshare-v*")
    path = glob.glob(mmshare_build_exp)
    if len(path) == 0:
        raise ValueError("No mmshare build found")
    return path[0]


def _is_valid_repo(repo):
    full_path = os.path.join(SCHRODINGER_SRC, repo)
    return os.path.isdir(full_path) and repo in REPOS


def __get_modified_files(repo, diff_generator="HEAD"):
    if not _is_valid_repo(repo):
        raise ValueError("Invalid repo: {}".format(repo))
    git_command = f"git diff --name-only {diff_generator}"
    output = subprocess.check_output(git_command.split())
    return output.decode("utf-8").strip().split("\n")


def _is_clang_supported(file):
    cpp_extensions = [".cpp", ".h", ".cxx", ".c", ".hpp"]
    return any(file.endswith(extension) for extension in cpp_extensions)


def _is_yapf_supported(file):
    return file.endswith(".py") or file.endswith("wscript")


def format_files_from_repo(repo):
    modified_files = __get_modified_files(repo)
    yapf_supported_files = [
        file for file in modified_files if _is_yapf_supported(file)
    ]
    clang_supported_files = [
        file for file in modified_files if _is_clang_supported(file)
    ]
    if yapf_supported_files:
        yapf_command = YAPF_CMD + yapf_supported_files
        subprocess.call(yapf_command)
        flake_command = FLAKE_CMD + yapf_supported_files
        subprocess.call(flake_command)
    if clang_supported_files:
        clang_command = CLANG_CMD + clang_supported_files
        subprocess.call(clang_command)


def build_mmshare_python():
    mmshare_build_dir = get_mmshare_build_dir()
    python_build_dir = os.path.join(mmshare_build_dir, "python")
    make_install = "make install"
    with cd_dir(python_build_dir):
        subprocess.call(make_install.split())
    python_test_dir = os.path.join(mmshare_build_dir, "python", "test")
    with cd_dir(python_test_dir):
        subprocess.call(make_install.split())


def build_maestro_without_test():
    with cd_dir(MAESTRO_SRC_PATH):
        build_cmd = WAFBUILD + " --target=maestro"
        subprocess.call(build_cmd, env=os.environ, shell=True)


def __main__():
    print(format_files_from_repo(MAESTRO_SRC))


if __name__ == '__main__':
    __main__()
