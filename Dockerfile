FROM		centos:centos7
MAINTAINER 	JAkub Scholz "www@scholzj.com"

ARG FTP_USERNAME
ARG FTP_PASSWORD
ARG FTP_HOSTNAME

# Install all qpid dependencies
USER root

RUN yum -y install epel-release
RUN yum -y install  ncftp

RUN yum -y install epel-release
RUN yum -y install wget tar rpm-build rpmdevtools gcc gcc-c++ cmake make libuv-devel libuuid-devel openssl-devel swig python-devel ruby-devel php-devel perl-devel java-1.8.0-openjdk-devel epydoc doxygen perl-Test-Exception.noarch perl-Test-Simple.noarch cyrus-sasl.x86_64 cyrus-sasl-devel.x86_64 cyrus-sasl-plain.x86_64 cyrus-sasl-md5.x86_64 createrepo ncftp

RUN rpmdev-setuptree
WORKDIR /root/rpmbuild/SOURCES
RUN wget https://github.com/apache/qpid-proton/archive/0.20.0-rc1.tar.gz
RUN tar -xf 0.20.0-rc1.tar.gz
RUN mv qpid-proton-0.20.0-rc1/ qpid-proton-0.20.0/
RUN tar -z -cf qpid-proton-0.20.0.tar.gz qpid-proton-0.20.0/
RUN rm -rf 0.20.0-rc1.tar.gz qpid-proton-0.20.0/
WORKDIR /root/rpmbuild/SPECS
ADD ./qpid-proton.spec /root/rpmbuild/SPECS/qpid-proton.spec
RUN rpmbuild -ba qpid-proton.spec

# Create and deploy the RPMs to the repository
RUN mkdir -p /root/repo/CentOS/7/x86_64
RUN mkdir -p /root/repo/CentOS/7/SRPMS
RUN mv /root/rpmbuild/RPMS/x86_64/*.rpm /root/repo/CentOS/7/x86_64/
RUN mv /root/rpmbuild/RPMS/noarch/*.rpm /root/repo/CentOS/7/x86_64/
RUN mv /root/rpmbuild/SRPMS/*.rpm /root/repo/CentOS/7/SRPMS/
WORKDIR /root/repo/CentOS/7/x86_64/
RUN createrepo .
WORKDIR /root/repo/CentOS/7/SRPMS
RUN createrepo .

RUN ncftpget -u $FTP_USERNAME -p $FTP_PASSWORD -R -DD $FTP_HOSTNAME /tmp/ /web/repo/qpid-proton-testing/
RUN ncftpput -u $FTP_USERNAME -p $FTP_PASSWORD -R $FTP_HOSTNAME /web/repo/qpid-proton-testing/ /root/repo/*

# Nothing to run
CMD    /bin/bash
