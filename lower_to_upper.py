# Update lower case $user to upper case $USER in local environment

import logging
import py
import yaml
import temporary
import os
import sys
from datetime import datetime  # timedelta
import re
import requests

lhost_url = 'http://161.85.111.157/svn/ibc/sites/ARJUN/lhost.yml'
'''
http_proxy = "http://165.225.96.34:9480"
https_proxy = "http://165.225.96.34:9480"
proxyDict = {
    "http": http_proxy,
    "https": https_proxy
}
'''
'''
os.environ['HTTP_PROXY'] = "http://165.225.96.34:9480"
os.environ['HTTPS_PROXY'] = "http://165.225.96.34:9480"
'''
LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
LOG_FORMAT = '%(asctime)s.%(msecs).06dZ - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FILE_NAME = 'svn_changes-{dt}.log'.format(dt=datetime.now().strftime("%d-%m-%Y"))
IBC = {
    # 'SVN_URL': 'http://10.171.22.33/svn/ibc/sites/',
    'SVN_URL': 'http://161.85.111.157/svn/ibc/sites/',
    'SVN_USERNAME': 'operator',
    'SVN_PASSWORD': 'st3nt0r'
}


def get_logger():
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    return logging


log = get_logger()
failed_sites = []


class MyDumper(yaml.Dumper):  # your force-indent dumper

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


class LhostYmlFileChangerForMultipleSites():
    def __init__(self):
        pass
        self.keyName1 = '$user'
        # self.keyName2 = 'USER112'

    def change_values_for_all_sites(self, site_list):  # new_value_for_keyname1, new_value_for_keyname2):
        for site in site_list:
            try:
                self.change_values_for_one_site(site)  # new_value_for_keyname1, new_value_for_keyname2)
            except Exception as e:
                log.error('while updating the {site} error occured:\n {e}'.format(site=site, e=e))
                failed_sites.append(site)

    def change_values_for_one_site(self, site):  # new_value_for_keyname1, new_value_for_keyname2):
        self.set_site_svn_lhost_path(site)
        self.set_subpath_siteid(site)
        with temporary.temp_dir(parent_dir='/tmp/') as tmp_work_dir:
            teml_yml_fl = str(tmp_work_dir) + '/{site}/lhost.yml'.format(site=site)
            print teml_yml_fl
            self.set_work_dir(tmp_work_dir)
            self.wc.info()
            with open(teml_yml_fl) as scanner_conts:
                lhost_yml_dict = yaml.load(scanner_conts)
                # print lhost_yml_dict
                lhost_yml_dict['endpoints'] = lhost_yml_dict.get('endpoints', {})
                lhost_yml_dict['endpoints'] = re.sub('(\$user)+', '$USER', lhost_yml_dict['endpoints'], flags=re.M | re.IGNORECASE)
                print lhost_yml_dict['endpoints']
                # print lhost_yml_dict['endpoints']
                # r = requests.get(lhost_url, auth=('operator', 'st3nt0r'))
                # with open('Arjun_Lhost.yml', 'w') as f:
                #    f.write(r.content)
                # lhost_yml_dict['shinken_resources'][self.keyName1] = self.encrypt(new_value_for_keyname1)
                # lhost_yml_dict['shinken_resources'][self.keyName2] = self.encrypt(site.upper() + new_value_for_keyname2)
            self.process_config_file('/lhost.yml', yaml.safe_dump(lhost_yml_dict, default_flow_style=False, Dumper=MyDumper))
            self.log_status()
            revision = self.wc.commit(msg='Updated lhost details of siteid:%s as part of %s on %s' % (site, 'FCO12345678', datetime.now()))  # FCO12345678
            if revision:
                log.info('revision: %s', str(revision))
            else:
                log.debug('No changes, nothing to commit')

    def set_site_svn_lhost_path(self, siteid):
        self.lhost_site_uri_path = IBC['SVN_URL'] + "{siteid}".format(siteid=siteid)

    def get_site_svn_lhost_path(self):
        return self.lhost_site_uri_path

    @property
    def wc(self):
        return self.setup_wc()

    def set_subpath_siteid(self, siteid):
        self.subpath = siteid

    def get_subpath_siteid(self):
        return self.subpath

    def set_work_dir(self, work_dir):
        self.work_dir = str(work_dir)

    def get_work_dir(self):
        return self.work_dir

    def get_subpath_wc(self):
        return os.path.join(self.get_work_dir(), self.get_subpath_siteid())

    def get_svn_auth(self):
        self.sites_root_url = IBC['SVN_URL']
        return py.path.SvnAuth(IBC['SVN_USERNAME'], IBC['SVN_PASSWORD'], cache_auth=False, interactive=False)

    @property
    def subpath_url(self):
        return os.path.join(self.sites_root_url, self.get_subpath_siteid())

    def setup_wc(self):
        auth = self.get_svn_auth()
        subpath_svn_url = self.subpath_url
        wc = py.path.svnwc(self.get_subpath_wc())
        wc.auth = auth
        wc.checkout(subpath_svn_url)
        return wc

    def log_status(self):
        status = self.wc.status(rec=1)
        attr_to_list = ['added', 'deleted', 'modified', 'conflict', 'unknown']
        for attr in attr_to_list:
            svnwc_files_with_attr = getattr(status, attr)
            with_attr_filenames = [item.strpath for item in svnwc_files_with_attr]
            log.info('%s files: %s', attr, str(with_attr_filenames))

    def process_config_file(self, filename, content):
        if content is None:
            file_to_remove = self.wc.join(filename)
            if file_to_remove.check():
                file_to_remove.remove()
        else:
            file_to_write = self.wc.ensure(filename)
            file_to_write.write(content)


def replace_user(datafile):
    with open(datafile, 'r') as f:
        s = f.read()

    with open(datafile, 'w') as f:
        z = re.sub('(\$user)+', '$USER', s, flags=re.M | re.IGNORECASE)
        f.write(z)


def main():
    # datafile = 'SiteInfoCopy.txt'
    m = LhostYmlFileChangerForMultipleSites()
    # print m
    sites_list_in_ALLCAPS = []  # Be sure to use only Valid sites and all Sites are capital
    try:  # Try to get all the site id from a file
        with open("sites.txt", 'r') as sites_file:  # Index Error occur if sites file is not provided
            for line in sites_file:
                sites_list_in_ALLCAPS.append(line.rstrip('\n'))
                print sites_list_in_ALLCAPS
        # replace_user(datafile)
        # new_value_for_user111 = 'IDM_user'  # updated value for the key in plain text
        # appended_string_for_user112 = '$n1mD@1P@D19'  # updated value for the key in plain text
        m.change_values_for_all_sites(sites_list_in_ALLCAPS)  # new_value_for_user111, appended_string_for_user112)
        # print m
        sites_list_in_lowercase = map(lambda x: x.lower(), sites_list_in_ALLCAPS)
        # print sites_list_in_lowercase
        m.change_values_for_all_sites(sites_list_in_lowercase)  # new_value_for_user111, appended_string_for_user112)
        # print m
        if not failed_sites:
            print 'All Sites Updated Successfully'
        else:
            print 'the following sites failed to update:\t', failed_sites
    except IndexError:
        print "Error: Please provide sites file as the second argument"


if __name__ == '__main__':
    main()
