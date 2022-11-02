import datetime
import os
import platform
import shutil
import subprocess

from app.utils.types import OsType


class SystemUtils:

    @staticmethod
    def get_used_of_partition(path):
        """
        获取系统存储空间占用信息
        """
        if not path:
            return 0, 0
        if not os.path.exists(path):
            return 0, 0
        try:
            total_b, used_b, free_b = shutil.disk_usage(path)
            return used_b, total_b
        except Exception as e:
            print(str(e))
            return 0, 0

    @staticmethod
    def get_system():
        """
        获取操作系统类型
        """
        if platform.system() == 'Windows':
            return OsType.WINDOWS
        else:
            return OsType.LINUX

    @staticmethod
    def get_free_space_gb(folder):
        """
        计算目录剩余空间大小
        """
        total_b, used_b, free_b = shutil.disk_usage(folder)
        return free_b / 1024 / 1024 / 1024

    @staticmethod
    def get_local_time(utc_time_str):
        """
        通过UTC的时间字符串获取时间
        """
        try:
            utc_date = datetime.datetime.strptime(utc_time_str.replace('0000', ''), '%Y-%m-%dT%H:%M:%S.%fZ')
            local_date = utc_date + datetime.timedelta(hours=8)
            local_date_str = datetime.datetime.strftime(local_date, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f'Could not get local date:{e}')
            return utc_time_str
        return local_date_str

    @staticmethod
    def check_process(pname):
        """
        检查进程序是否存在
        """
        if not pname:
            return False
        text = subprocess.Popen('ps -ef | grep -v grep | grep %s' % pname, shell=True).communicate()
        return True if text else False

    @staticmethod
    def execute(cmd):
        """
        执行命令，获得返回结果
        """
        return os.popen(cmd).readline().strip()

    @staticmethod
    def is_docker():
        return os.path.exists('/.dockerenv')

    @staticmethod
    def copy(src, dest):
        """
        复制
        """
        try:
            shutil.copy2(os.path.normpath(src), os.path.normpath(dest))
            return 0, ""
        except Exception as err:
            return -1, str(err)

    @staticmethod
    def move(src, dest):
        """
        移动
        """
        try:
            tmp_file = os.path.normpath(os.path.join(os.path.dirname(src),
                                                     os.path.basename(dest)))
            os.rename(os.path.normpath(src), tmp_file)
            shutil.move(tmp_file, os.path.normpath(dest))
            return 0, ""
        except Exception as err:
            return -1, str(err)

    @staticmethod
    def link(src, dest):
        """
        硬链接
        """
        try:
            os.link(os.path.normpath(src), os.path.normpath(dest))
            return 0, ""
        except Exception as err:
            return -1, str(err)

    @staticmethod
    def softlink(src, dest):
        """
        软链接
        """
        try:
            os.symlink(os.path.normpath(src), os.path.normpath(dest))
            return 0, ""
        except Exception as err:
            return -1, str(err)

    @staticmethod
    def rclone_move(src, dest):
        """
        Rclone移动
        """
        try:
            src = os.path.normpath(src)
            dest = dest.replace("\\", "/")
            st = subprocess.STARTUPINFO()
            st.dwFlags = subprocess.STARTF_USESHOWWINDOW
            st.wShowWindow = subprocess.SW_HIDE
            retcode = subprocess.run(['rclone', 'moveto',
                                      src,
                                      f'NASTOOL:{dest}'], startupinfo=st).returncode
            return retcode, ""
        except Exception as err:
            return -1, str(err)

    @staticmethod
    def rclone_copy(src, dest):
        """
        Rclone复制
        """
        try:
            src = os.path.normpath(src)
            dest = dest.replace("\\", "/")
            st = subprocess.STARTUPINFO()
            st.dwFlags = subprocess.STARTF_USESHOWWINDOW
            st.wShowWindow = subprocess.SW_HIDE
            retcode = subprocess.run(['rclone', 'copyto',
                                      src,
                                      f'NASTOOL:{dest}'], startupinfo=st).returncode
            return retcode, ""
        except Exception as err:
            return -1, str(err)

    @staticmethod
    def minio_move(src, dest):
        """
        Minio移动
        """
        try:
            src = os.path.normpath(src)
            dest = dest.replace("\\", "/")
            if dest.startswith("/"):
                dest = dest[1:]
            st = subprocess.STARTUPINFO()
            st.dwFlags = subprocess.STARTF_USESHOWWINDOW
            st.wShowWindow = subprocess.SW_HIDE
            retcode = subprocess.run(['mc', 'mv',
                                      '--recursive',
                                      src,
                                      f'NASTOOL/{dest}'], startupinfo=st).returncode
            return retcode, ""
        except Exception as err:
            return -1, str(err)

    @staticmethod
    def minio_copy(src, dest):
        """
        Minio复制
        """
        try:
            src = os.path.normpath(src)
            dest = dest.replace("\\", "/")
            if dest.startswith("/"):
                dest = dest[1:]
            st = subprocess.STARTUPINFO()
            st.dwFlags = subprocess.STARTF_USESHOWWINDOW
            st.wShowWindow = subprocess.SW_HIDE
            retcode = subprocess.run(['mc', 'cp',
                                      '--recursive',
                                      src,
                                      f'NASTOOL/{dest}'], startupinfo=st).returncode
            return retcode, ""
        except Exception as err:
            return -1, str(err)

    @staticmethod
    def get_windows_drives():
        """
        获取Windows所有盘符
        """
        vols = []
        for i in range(65, 91):
            vol = chr(i) + ':'
            if os.path.isdir(vol):
                vols.append(vol)
        return vols
