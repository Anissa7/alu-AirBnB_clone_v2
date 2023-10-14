#!/usr/bin/python3
"""
script that distributes an archive to my web servers,
using the function (do_deploy:)
"""
import os
from fabric.api import put, run, env
env.hosts = ['34.230.10.59', '54.92.193.250']


def do_deploy(archive_path):
    """OOB
    Distribution to my servers
    """
    if archive_path is None or not os.path.exists(archive_path):
        return False
    try:
        file = archive_path.split("/")[-1]
        file_name = file.split(".")[0]
        path = "/data/web_static/releases/"
        # upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # create a folder with the same name as the archive
        # without the extension
        run("mkdir -p {}{}/".format(path, file_name))
        # uncompress the archive to the folder
        run("tar -xzf /tmp/{} -C {}{}/".format(
            file, path, file_name))
        # delete the archive from the web server
        run("rm /tmp/{}".format(file))
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, file_name))
        # delete the symbolic link /data/web_static/current from the web server
        run("rm -rf {}{}/web_static".format(path, file_name))
        run("rm -rf /data/web_static/current")
        # create new symbolic link /data/web_static/current on web server
        # linked to the new version of your code
        run("ln -s {}{}/ /data/web_static/current".
            format(path, file_name))
        return True
    except BaseException:
        return False
