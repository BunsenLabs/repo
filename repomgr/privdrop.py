import logging
import os
import pwd

logger = logging.getLogger(__name__)

def privhave() -> bool:
    """ Ensure that we are root as we are expecting to modify the
    package manager configuration. """
    if (euid := os.geteuid()) != 0:
        logger.error("privhave: running with euid=%d, expected 0", euid)
        return False
    return True

def privdrop(user: str = "_apt") -> bool:
    olduid = os.getuid()

    if user == "root":
        logger.debug("privdrop: privdropping to root makes no sense")
        return False

    if olduid != 0:
        logger.debug("privdrop: uid (%d) is not 0, already done", olduid)
        return True

    try:
        passwd = pwd.getpwnam(user)
        gidconf = (passwd.pw_gid, passwd.pw_gid, passwd.pw_gid,)
        uidconf = (passwd.pw_uid, passwd.pw_uid, passwd.pw_uid,)
        os.setresgid(*gidconf)
        assert os.getresgid() == gidconf
        os.setresuid(*uidconf)
        assert os.getresuid() == uidconf
    except KeyError:
        logger.error("privdrop: user %s does not exit in passwd database", user)
        return False
    except Exception as err:
        logger.error("privdrop: failed to privdrop: %s", err)
        return False

    return True

if __name__ == "__main__":
    print(privdrop())
