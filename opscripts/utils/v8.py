# vim: set fileencoding=utf-8 :

"""OpScripts utilities library
"""

# Standard Library
from __future__ import absolute_import, division, print_function
from signal import signal, SIGPIPE, SIG_DFL
import grp
import logging
import os
import pwd
import random
import re
import select
import subprocess
import sys
import tempfile
import traceback


LOG = logging.getLogger(__name__)
# Ignore SIG_PIPE and don't throw exceptions on it...
# http://newbebweb.blogspot.com/2012/02/python-head-ioerror-errno-32-broken.html
signal(SIGPIPE, SIG_DFL)


class Fatal(Exception):
    def __init__(self, message, code=None):
        self.code = code if code else 1
        message = "({0}) {1}".format(self.code, message)
        super(Fatal, self).__init__(message)


def _exec_cmd_base(cmd_args, cwd=None, uid=None, gids=None):
    """INTERNAL/PRIVATE
    Execute specified command with optional working directory, uid, and gids.

    Returns exit status, STDOUT, and STDERR.
    """
    try:
        int(gids)
        gids = [gids, ]
    except TypeError:
        pass
    if gids is not None:
        gids = list(gids)
        gids.sort()

    def switch_uid_gids():
        egids = os.getgroups()
        egids.sort()
        euid = os.geteuid()
        if gids is not None and gids != egids:
            os.setgroups(gids)
        if uid is not None and uid != euid:
            os.seteuid(uid)

    job = subprocess.Popen(cmd_args, cwd=cwd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           preexec_fn=switch_uid_gids)
    exit_status = job.wait()
    stdout = job.stdout.read().strip().decode("utf-8")
    job.stdout.close()
    stderr = job.stderr.read().strip().decode("utf-8")
    job.stderr.close()
    return [exit_status, stdout, stderr]


def _exec_cmd_base_spec(cmd_args, cwd=None, uid=None, gids=None):
    """INTERNAL/PRIVATE
    Assembles a string description of the specified command and returns it.
    """
    cmd_spec = "Executing {0}".format(cmd_args)
    if cwd is not None:
        cmd_spec = "{0} within {1}".format(cmd_spec, cwd)
    if uid is not None:
        euid = uid
    else:
        euid = os.getuid()
    if gids is not None:
        try:
            int(gids)
            gids = [gids, ]
        except TypeError:
            pass
        egids = gids
    else:
        egids = os.getgroups()
    egids = ", ".join(map(str, egids))
    cmd_spec = "{0} as {1}:({2})".format(cmd_spec, euid, egids)
    return cmd_spec


def _check_logging():
    """INTERNAL/PRIVATE
    Check for logging handlers.
    """
    if LOG.handlers:
        return True
    elif logging.getLogger().handlers:
        return True
    return False


def _get_gids(username, gid):
    """INTERNAL/PRIVATE
    Get supplemental group ids from group database.
    """
    gids = set()
    try:
        gids.add(int(gid))
    except ValueError:
        pass
    try:
        for grp_entry in grp.getgrall():
            if username in grp_entry.gr_mem:
                gids.add(grp_entry.gr_gid)
    except KeyError:
        pass
    gids = list(gids)
    gids.sort()
    return gids


def _get_ids_from_uid(potential_uid):
    """INTERNAL/PRIVATE
    Get uid and gids from supplied uid.
    """
    uid, gid, gids = (None, None, None)
    try:
        uid = int(potential_uid)
        try:
            pwd_entry = pwd.getpwuid(uid)
            username = pwd_entry.pw_name
            gid = pwd_entry.pw_gid
            gids = _get_gids(username, gid)
        except KeyError:
            pass
    except ValueError:
        pass
    return uid, gids


def _get_ids_from_username(username):
    """INTERNAL/PRIVATE
    Get uid and gids from supplied username.
    """
    uid, gid, gids = (None, None, None)
    try:
        username = str(username)
        pwd_entry = pwd.getpwnam(username)
        uid = pwd_entry.pw_uid
        gid = pwd_entry.pw_gid
        gids = _get_gids(username, gid)
    except KeyError:
        pass
    return uid, gids


def _get_ids_from_sudo_env():
    """INTERNAL/PRIVATE
    Get uid and gids from sudo environment variables.
    """
    uid, gid, gids = (None, None, None)
    if "SUDO_UID" in os.environ and os.environ["SUDO_UID"] != "":
        uid = int(os.environ["SUDO_UID"])
        try:
            pwd_entry = pwd.getpwuid(uid)
        except KeyError:
            return uid, gids
        username = pwd_entry.pw_name
        if "SUDO_GID" in os.environ and os.environ["SUDO_GID"] != "":
            gid = int(os.environ["SUDO_GID"])
        else:
            try:
                gid = pwd_entry.pw_gid
            except KeyError:
                pass
        if gid is not None:
            gids = _get_gids(username, gid)
    return uid, gids


def atomic_replace_file(file_orig, content, follow_symlink=False):
    """Replaces the original content with new content, maintaining
    file ownership/perms if executed with sufficient privileges.

    :param file - Full path to file
    :param content - String to be written as new content
    """
    file_orig_abs = os.path.abspath(file_orig)
    file_orig_real = os.path.realpath(file_orig)
    if not follow_symlink and file_orig_abs != file_orig_real:
        LOG.debug("Refusing to replace file with symlink in path: {0}"
                  .format(file_orig))
        return False

    file_dir = os.path.dirname(file_orig)
    if os.path.isfile(file_orig):
        orig_stat = os.stat(file_orig)
        orig_perms = orig_stat.st_mode & 0o777
        orig_uid = orig_stat.st_uid
        orig_gid = orig_stat.st_gid
    else:
        LOG.warn("No original file to replace. New file may not have expected"
                 " permissions or ownership")
        orig_stat = False

    # Create temp file
    file_temp_name = write_tempfile(file_dir, content)

    if orig_stat:
        # Change ownershipo and permissions to match original
        os.chown(file_temp_name, orig_uid, orig_gid)
        os.chmod(file_temp_name, orig_perms)

        # Backup file
        file_backup = back_up_file(file_orig)

    # Attempt swap
    if orig_stat:
        LOG.debug("Unlinking original file: {0}".format(file_orig_real))
        os.unlink(file_orig)
    try:
        LOG.debug("Linking temp file to original file location")
        os.link(file_temp_name, file_orig)
        if orig_stat:
            LOG.debug("Deleting backup file")
            os.unlink(file_backup)
        LOG.debug("Deleting temp file")
        os.unlink(file_temp_name)
        return True
    except:
        if orig_stat:
            LOG.error("Linking temp file failed. Linking backup file to"
                      " original file location and removing backup file")
            os.link(file_backup, file_orig)
            os.unlink(file_backup)
        LOG.debug("Deleting temp file")
        os.unlink(file_temp_name)
        return False


def back_up_file(file_path, target_dir=None, suffix="_orig"):
    """Create a backup of a file, via os.link. Will not clobber
    existing backups. If no target directory is supplied, will
    use directory of file to be backed up.

    :param file - Full or relative path to file requiring backup
    :param target_dir - Where to put the backup
    :param suffix - Suffix to apply to differentiate backup
    """
    if target_dir is None:
        target_dir = os.path.dirname(os.path.abspath(file_path))

    try:
        _, filename = os.path.split(file_path)
    except AttributeError as e:
        LOG.error(e)
        return False

    if not filename:
        LOG.error("Invalid file supplied for backup: {0}".format(file_path))
        return False

    file_backup = os.path.join(target_dir, filename + suffix)

    try:
        LOG.debug("Linking original file to backup file: {0}"
                  .format(file_backup))
        os.link(file_path, file_backup)
    except OSError as e:
        LOG.error(e)
        return False

    return file_backup


def exec_cmd_fail_hard(cmd_args, cwd=None, uid=None, gids=None):
    """Execute a command and Fatal if it fails (as well as print STDERR).

    Returns exit status, STDOUT, and STDERR.
    """
    cmd_spec = _exec_cmd_base_spec(cmd_args, cwd, uid, gids)
    results = _exec_cmd_base(cmd_args, cwd, uid, gids)
    if results[0] != 0:
        LOG.error("STDERR: {0}".format(results[2]))
        raise Fatal("{0} failed ({1}).".format(cmd_spec, results[0]),
                    results[0])
    return results


def exec_cmd_fail_prompt(cmd_args, cwd=None, uid=None, gids=None,
                         opt_force=None, opt_yes=None):
    """Execute a command and if it fails:
    - Quit if opt_yes is True
    - Continue if opt_force is True
    - Prompt to continue

    Returns exit status, STDOUT, and STDERR.
    """
    cmd_spec = _exec_cmd_base_spec(cmd_args, cwd, uid, gids)
    results = _exec_cmd_base(cmd_args, cwd, uid, gids)
    if results[0] != 0:
        LOG.error("STDERR: {0}".format(results[2]))
        if opt_force:
            LOG.debug("{0} failed ({1}). Force option used. Continuing."
                      .format(cmd_spec, results[0]))
        elif opt_yes:
            raise Fatal("{0} failed ({1}). Yes option used. Exiting."
                        .format(cmd_spec, results[0]), results[0])
        else:
            LOG.error("{0} failed ({1})".format(cmd_spec, results[0]))
            request_y_to_continue()
    return results


def exec_cmd_debug(cmd_args, cwd=None, uid=None, gids=None):
    """Execute a command and provide all available information about it via
    debug.

    Returns exit status, STDOUT, and STDERR.
    """
    cmd_spec = _exec_cmd_base_spec(cmd_args, cwd, uid, gids)
    LOG.debug(cmd_spec)
    results = _exec_cmd_base(cmd_args, cwd, uid, gids)
    LOG.debug("exit status: {0}".format(results[0]))
    LOG.debug("STDOUT: {0}".format(results[1]))
    LOG.debug("STDERR: {0}".format(results[2]))
    return results


def format_columns(rows, align=None):
    """Convert a list (rows) of lists (columns) to a formatted list of lines.
    When joined with newlines and printed, the output is similar to
    `column -t`.

    The optional align may be a list of alignment formatters.

    The last (right-most) column will not have any trailing whitespace so that
    it wraps as cleanly as possible.

    Based on solution provided by antak in http://stackoverflow.com/a/12065663
    """
    lines = list()
    widths = [max(map(len, map(str, col))) for col in zip(*rows)]
    for row in rows:
        formatted = list()
        last_col = len(row) - 1
        for i, col in enumerate(row):
            # right alighed
            if align and align[i].lower() in (">", "r"):
                formatted.append(str(col).rjust(widths[i]))
            # center aligned
            elif align and align[i].lower() in ("^", "c"):
                col_formatted = str(col).center(widths[i])
                if i == last_col:
                    col_formatted = col_formatted.rstrip()
                formatted.append(col_formatted)
            # left aligned
            else:
                if i == last_col:
                    formatted.append(str(col))
                else:
                    formatted.append(str(col).ljust(widths[i]))
        lines.append("  ".join(formatted))
    return lines


def get_non_root_ids(username_or_uid, fallback_uid, fallback_gids):
    """Determine uid and gids that should be used for user (non-root) exec.

    1. Try to determine uid and gids assuming input is uid
    2. Try to determine uid and gids assuming input is username
    3. Try to use SUDO_UID and SUDO_GID or SUDO_UID
    4. Use fallback uid and gids
    """
    uid, gids = (None, None)
    try:
        int(fallback_gids)
        fallback_gids = [fallback_gids, ]
    except TypeError:
        pass
    if username_or_uid not in (None, 0, ""):
        # 1. Try to determine uid and gid assuming input is uid
        uid, gids = _get_ids_from_uid(username_or_uid)
        # 2. Try to determine uid and gid assuming input is username
        if uid in (None, 0) or gids is None or 0 in gids:
            uid, gids = _get_ids_from_username(username_or_uid)
    # 3. Try to use SUDO_UID and SUDO_GID or SUDO_UID and account database
    if uid in (None, 0) or gids is None or 0 in gids:
        uid, gids = _get_ids_from_sudo_env()
    # 4. Use fallback uid and gid
    if uid in (None, 0) or gids is None or 0 in gids:
        uid, gids = (fallback_uid, fallback_gids)
    return uid, gids


def is_valid_hostname(hostname):
    """Validate hostname syntax:
    - Entire hostname must
        - not exceed 253 characters
        - not be all-numeric (so that it can't be confused with an IP address)
    - Each label must:
      - contain at least 1 and not more than 63 characters
      - not begin or end with a hyphen
      - not contain illegal characters

    http://stackoverflow.com/questions/2532053/validate-a-hostname-string
    """
    disallowed = re.compile(r"[^A-Z\d-]", re.IGNORECASE)
    # strip exactly one dot from the right, if present
    if hostname.endswith("."):
        hostname = hostname[:-1]
    # hostname must not exceed 253 characters
    if len(hostname) > 253:
        return False
    # hostnbame must be not all-numeric (so that it can't be confused with an
    # IP address)
    if re.match(r"[\d.]+$", hostname):
        return False
    for label in hostname.split("."):
        # label must contain at least 1 and not more than 63 characters
        if len(label) == 0 or len(label) > 63:
            return False
        # label must not begin or end with a hyphen
        if label.startswith("-") or label.endswith("-"):
            return False
        # label must not contain illegal characters
        if disallowed.search(label):
            return False
    return True


def log_ctrlc_and_exit():
    print(file=sys.stderr)
    if _check_logging():
        LOG.info("(130) Halted via KeyboardInterrupt.")
    else:
        print("CRITICAL No handlers could be found for logger \"{0}\""
              .format(__name__), file=sys.stderr)
        print("INFO (130) Halted via KeyboardInterrupt.", file=sys.stderr)
    sys.exit(130)


def log_exception():
    if _check_logging():
        LOG.exception("Unhandled exception:")
    else:
        print("CRITICAL No handlers could be found for logger \"{0}\""
              .format(__name__), file=sys.stderr)
        print("ERROR Unhandled exception:\n{0}".format(traceback.print_exc()),
              file=sys.stderr)


def log_exception_and_exit(exit_status=1):
    log_exception()
    sys.exit(exit_status)


def log_fatal_and_exit():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if _check_logging():
        LOG.critical(exc_value)
    else:
        print("CRITICAL No handlers could be found for logger \"{0}\""
              .format(__name__), file=sys.stderr)
        print("CRITICAL {0}".format(exc_value), file=sys.stderr)
    sys.exit(exc_value.code)


def request_confirmation(timeout=30):
    """Request the operator input the displayed random number to confirm the
    script should make the changes requested. Each attempt fails if the
    timeout is reached.

    Exits with an error after five failures.
    """
    try:
        timeout = float(timeout)
    except:
        raise Fatal("request_confirmation timeout must be a number",
                    os.EX_NOPERM)
    random_int = random.randint(10000, 99999)
    message = ("To continue, please enter the number '%d' within %d"
               " seconds:" % (random_int, timeout))
    i = 0
    while i < 5:
        i += 1
        print(message,)
        read_obj, w, x = select.select([sys.stdin], list(), list(), timeout)
        if read_obj:
            response = sys.stdin.readline().strip()
            try:
                response = int(response)
            except ValueError:
                pass
            except:
                raise
            if response == random_int:
                return
    raise Fatal("Failed to provide confirmation input.", os.EX_NOPERM)


def request_y_to_continue(timeout=30):
    """Request the operator input "y" to continue. Each attempt fails if the
    timeout is reached.

    Exits with an error after five failures.
    """
    try:
        timeout = float(timeout)
    except:
        raise Fatal("request_confirmation timeout must be a number",
                    os.EX_NOPERM)
    message = "Do you want to continue? (y/n):"
    i = 0
    while i < 5:
        i += 1
        print(message,)
        read_obj, w, x = select.select([sys.stdin], list(), list(), timeout)
        if read_obj:
            response = sys.stdin.readline().strip()[0:].lower()
            try:
                response = str(response)
            except ValueError:
                pass
            except:
                raise
            if response == "y":
                return
            elif response == "n":
                raise Fatal("Response received: \"{0}\". Exiting."
                            .format(response))
    raise Fatal("Failed to provide confirmation input.", os.EX_NOPERM)


def verify_root():
    """Verify script is being run as root.
    """
    if not os.geteuid() == 0:
        raise Fatal("Must be root or equivalent (ex. sudo).", os.EX_NOPERM)


def write_tempfile(directory, content):
    file_temp_fd, file_temp_name = tempfile.mkstemp(dir=directory)
    LOG.debug("Created temp file: {0}".format(file_temp_name))
    file_temp_fo = os.fdopen(file_temp_fd, "w")
    file_temp_fo.writelines(content)
    file_temp_fo.close()

    return file_temp_name
