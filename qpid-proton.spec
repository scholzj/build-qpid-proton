%global proton_datadir %{_datadir}/proton-%{version}
%global gem_name qpid_proton

# per https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering#Preventing_files.2Fdirectories_from_being_scanned_for_deps_.28pre-scan_filtering.29
%global __provides_exclude_from ^%{_datadir}/proton-%{version}/examples/.*$
%global __requires_exclude_from ^%{_datadir}/proton-%{version}/examples/.*$

#  for older rpm, like el6, https://fedoraproject.org/wiki/EPEL:Packaging_Autoprovides_and_Requires_Filtering#Perl
%{?filter_setup:
%filter_provides_in %{_datadir}/proton-%{version}/examples/
%filter_requires_in %{_datadir}/proton-%{version}/examples/
%filter_setup
}

Name:           qpid-proton
Version:        0.30.0
Release:        SNAPSHOT%{?dist}
Summary:        A high performance, lightweight messaging library

License:        ASL 2.0
URL:            http://qpid.apache.org/proton/

Source0:        %{name}-%{version}.tar.gz

%if (0%{?fedora} || 0%{?rhel} == 7)
BuildRequires:  cmake >= 2.6
%global cmake_exe %{cmake}
%endif

%if 0%{?rhel} == 6
BuildRequires: cmake28
%global cmake_exe %{cmake28}
%endif

BuildRequires:  swig
BuildRequires:  pkgconfig
BuildRequires:  doxygen
BuildRequires:  libuuid-devel
BuildRequires:  openssl-devel
BuildRequires:  python
BuildRequires:  python-devel
BuildRequires:  epydoc
#BuildRequires:  perl(ExtUtils::MakeMaker)
#BuildRequires:  perl(Test::Exception)
#BuildRequires:  perl(Test::More)



%description
Proton is a high performance, lightweight messaging library. It can be used in
the widest range of messaging applications including brokers, client libraries,
routers, bridges, proxies, and more. Proton is based on the AMQP 1.0 messaging
standard. Using Proton it is trivial to integrate with the AMQP 1.0 ecosystem
from any platform, environment, or language.



%package c
Summary:   C libraries for Qpid Proton
Obsoletes: qpid-proton < %{version}-%{release}
Provides:  qpid-proton = %{version}-%{release}


%description c
%{summary}.


%files c
%defattr(-,root,root,-)
%dir %{proton_datadir}
%doc %{proton_datadir}/LICENSE.txt
%doc %{proton_datadir}/README.md
#%doc %{proton_datadir}/TODO
%{_libdir}/libqpid-proton.so.*
%{_libdir}/libqpid-proton-core.so.*
%{_libdir}/libqpid-proton-proactor.so.*


%post c -p /sbin/ldconfig

%postun c -p /sbin/ldconfig



%package c-devel
Requires:  qpid-proton-c%{?_isa} = %{version}-%{release}
Summary:   Development libraries for writing messaging apps with Qpid Proton
Obsoletes: qpid-proton-devel < %{version}-%{release}
Provides:  qpid-proton-devel = %{version}-%{release}


%description c-devel
%{summary}.


%files c-devel
%defattr(-,root,root,-)
%{_includedir}/proton
%{_libdir}/libqpid-proton.so
%{_libdir}/libqpid-proton-core.so
%{_libdir}/libqpid-proton-proactor.so
%{_libdir}/pkgconfig/libqpid-proton.pc
%{_libdir}/pkgconfig/libqpid-proton-cpp.pc
%{_libdir}/pkgconfig/libqpid-proton-core.pc
%{_libdir}/pkgconfig/libqpid-proton-proactor.pc
%{_libdir}/cmake/Proton
%{_libdir}/cmake/ProtonCpp
%doc %{proton_datadir}/examples

%package c-devel-doc
Summary:   Documentation for the C development libraries for Qpid Proton
BuildArch: noarch

%description c-devel-doc
%{summary}.

%files c-devel-doc
%defattr(-,root,root,-)
%doc %{proton_datadir}/docs/api-c



%package -n cpp-qpid-proton
Summary:  C++ language bindings for the Qpid Proton messaging framework

Requires: qpid-proton-c%{?_isa} = %{version}-%{release}

%description -n cpp-qpid-proton
%{summary}.


%files -n cpp-qpid-proton
%defattr(-,root,root,-)
%{_libdir}/libqpid-proton-cpp.so
%{_libdir}/libqpid-proton-cpp.so.*




%package -n cpp-qpid-proton-doc
Summary:   Documentation for the C++ language bindings for Qpid Proton
BuildArch: noarch


%description -n cpp-qpid-proton-doc
%{summary}.


%files -n cpp-qpid-proton-doc
%defattr(-,root,root,-)
%doc %{proton_datadir}/docs/api-cpp




%package -n python-qpid-proton
Summary:  Python language bindings for the Qpid Proton messaging framework

Requires: qpid-proton-c%{?_isa} = %{version}-%{release}
Requires: python


%description -n python-qpid-proton
%{summary}.


%files -n python-qpid-proton
%defattr(-,root,root,-)
%{python_sitearch}/_cproton.so
%{python_sitearch}/cproton.*
%{python_sitearch}/proton


%prep
%setup -q -n %{name}-%{version}


%build

%cmake_exe \
    -DPROTON_DISABLE_RPATH=true \
    -DPYTHON_SITEARCH_PACKAGES=%{python_sitearch} \
    -DNOBUILD_RUBY=1 \
    -DENABLE_FUZZ_TESTING=NO \
    -DSYSINSTALL_PYTHON=1 \
    -DCHECK_SYSINSTALL_PYTHON=0 \
    .
make all docs %{?_smp_mflags}



%install
%make_install

CPROTON_BUILD=$PWD . ./config.sh

chmod +x %{buildroot}%{python_sitearch}/_cproton.so
#find %{buildroot}%{proton_datadir}/examples/ -type f | xargs chmod -x


# clean up files that are not shipped
rm -rf %{buildroot}%{_exec_prefix}/bindings
rm -rf %{buildroot}%{_libdir}/java
rm -rf %{buildroot}%{_libdir}/libproton-jni.so
rm -rf %{buildroot}%{_datarootdir}/java
rm -rf %{buildroot}%{_libdir}/proton.cmake
rm -rf %{buildroot}%{proton_datadir}/tests
rm -rf %{buildroot}%{proton_datadir}/CMakeLists.txt

%changelog
* Wed Apr  8 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.9-3
- Added a global excludes macro to fix EL6 issues with example Perl modules.

* Wed Apr  8 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.9-2
- Marked the examples in -c-devel as doc.
- Turned off the executable flag on all files under examples.

* Mon Apr  6 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.9-1
- Rebased on Proton 0.9.
- Removed the proton binary from qpid-proton-c.
- Added the perl-qpid-proton subpackage.

* Tue Nov 18 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.8-1
- Rebased on Proton 0.8.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul  8 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.7-3
- Removed intra-package comments which cause error messages on package uninstall.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.7-1
- Rebased on Proton 0.7
- Added new CMake modules for Proton to qpid-proton-c-devel.

* Mon Feb 24 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.6-2
- Reorganized the subpackages.
- Merged up branches to get things back into sync.

* Thu Jan 16 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.6-1
- Rebased on Proton 0.6.
- Update spec to delete ruby and perl5 directories if Cmake creates them.
- Removed Java sub-packages - those will be packaged separate in future.

* Fri Sep  6 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.5-2
- Made python-qpid-proton-doc a noarch package.
- Resolves: BZ#1005058

* Wed Aug 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.5-1
- Rebased on Proton 0.5.
- Resolves: BZ#1000620

* Mon Aug 26 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-4
- Created the qpid-proton-c-devel-doc subpackage.
- Resolves: BZ#1000615

* Wed Jul 24 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-3
- Provide examples for qpid-proton-c
- Resolves: BZ#975723

* Fri Apr  5 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2.2
- Added Obsoletes and Provides for packages whose names changed.
- Resolves: BZ#948784

* Mon Apr  1 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2.1
- Fixed the dependencies for qpid-proton-devel and python-qpid-proton.

* Thu Mar 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-2
- Moved all C libraries to the new qpid-proton-c subpackage.

* Tue Feb 26 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.4-1
- Rebased on Proton 0.4.

* Thu Feb 21 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-4
- Fixes copying nested data.
- PROTON-246, PROTON-230

* Mon Jan 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-3
- Fixes build failure on non-x86 platforms.
- Resolves: BZ#901526

* Fri Jan 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-2
- Fixes build failure on non-x86 platforms.
- Resolves: BZ#901526

* Wed Jan 16 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.3-1
- Rebased on Proton 0.3.

* Fri Dec 28 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.4
- Moved ownership of the docs dir to the docs package.

* Wed Dec 19 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.3
- Fixed package dependencies, adding the release macro.

* Mon Dec 17 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.2
- Fixed subpackage dependencies on main package.
- Removed accidental ownership of /usr/include.

* Thu Dec 13 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2.1
- Remove BR for ruby-devel.
- Removed redundant package name from summary.
- Removed debugging artifacts from specfile.
- Moved unversioned library to the -devel package.
- Added dependency on main package to -devel.
- Fixed directory ownerships.

* Fri Nov 30 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-2
- Removed BR on help2man.
- Added patch for generated manpage.

* Mon Nov  5 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.2-1
- Initial packaging of the Qpid Proton.
