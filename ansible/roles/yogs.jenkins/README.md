Ye Olde Game Shoppe Jenkins role
================================

Setup Jenkins to run all the git hooks and tests for the project.

You need to setup SSL manually. I used
[letsencrypt](https://letsencrypt.readthedocs.org/en/latest/) for getting the
certificate and following
[this guide](https://github.com/letsencrypt/letsencrypt/issues/1701#issuecomment-163986593)
I converted it to JKS, the format used by Jenkins. Then you need to change the
relevant variables in /etc/sysconfig/jenkins.

Then after securing up Jenkins with logins and such you can create the task.
Something like this should work:

```
# Enable venv
# CentOS 7 has same problem as in
# http://askubuntu.com/questions/488529/pyvenv-3-4-error-returned-non-zero-exit-status-1
/usr/bin/pyvenv-3.4 --without-pip venv
source venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python
deactivate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python manage.py migrate
python manage.py jenkins
```
