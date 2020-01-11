from pyinfra import host
from pyinfra.modules import yum

SUDO = True

# Note: This "if" below is not really required.
# For instance, if you run this deploy on an
# Ubuntu instance (which does not use yum)
# the yum.packages() will simply be skipped
if host.fact.linux_name in ['CentOS', 'RedHat']:

    yum.packages(
        {'Install Vim and Vim enhanced'},
        ['vim-enhanced', 'vim'],
        update=True,
    )


if host.fact.linux_name == 'CentOS':
    yum.key(
        {'Add the Docker CentOS gpg key'},
        'https://download.docker.com/linux/{{ host.fact.lsb_release.id|lower }}/gpg',
    )

yum.rpm(
    {'Ensure an rpm is not installed'},
    'snappy',
    present=False,
)

if host.fact.linux_name in ['CentOS', 'RedHat']:

    packages = host.fact.rpm_packages
    epel_installed = False
    for p in packages.keys():
        if p.startswith('epel-release'):
            epel_installed = True

    if not epel_installed:
        yum.rpm(
            {'Install EPEL rpm to enable EPEL repo'},
            'https://dl.fedoraproject.org/pub/epel/epel-release-latest-'
            '{{  host.fact.linux_distribution.major }}.noarch.rpm',
            ignore_errors=True,
        )

    yum.packages(
        {'Install Zabbix and htop'},
        ['zabbix', 'htop'],
        update=True,
    )
