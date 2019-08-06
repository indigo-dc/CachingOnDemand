
Name: smartDecisionPlugin 
Version: 0.1.0
Release: 1%{?dist}
Summary: XCache plugin for smart decision service interaction 

Group: System Environment/Daemons
License: Apache
URL: https://github.com/cloud-pg/cachingondemand
Source0: %{name}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
# BuildRequires: xrootd-server-devel xerces-c-devel pcre-devel
BuildRequires: xrootd-server-devel pcre-devel
BuildRequires: cmake
# Requires: /usr/bin/xrootd pcre xerces-c
Requires: /usr/bin/xrootd pcre

%package devel
Summary: DUMMY
Group: System Environment/Development

%description
%{summary}

%description devel
%{summary}

%prep
%setup -q -c -n %{name}-%{version}

%build

%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo .
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/smartDecisionPlugin-4.so.*
%{_libdir}/smartDecisionPlugin-4.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/smartDecisionPlugin.hh

