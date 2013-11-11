Summary:	Caching HTTP download proxy for software packages
Name:		apt-cacher-ng
Version:	0.7.19
Release:	0.1
License:	Public domain
Group:		Development
Source0:	http://ftp.debian.org/debian/pool/main/a/apt-cacher-ng/%{name}_%{version}.orig.tar.xz
# Source0-md5:	f57a1323404d35f8668911907d9d026b
Source1:	%{name}.xinetd
URL:		http://www.unix-ag.uni-kl.de/~bloch/acng/
BuildRequires:	boost-devel
#BuildRequires:	bzlib-devel
BuildRequires:	libfuse-devel
BuildRequires:	libstdc++-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apt-Cacher NG is a caching HTTP download proxy for software packages,
primarily for Debian/Ubuntu clients. It's partially based on concepts
of Apt-Cacher but is rewritten with a main focus on performance and
low resource usage.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir}/%{name},%{_mandir}/man8,%{_sysconfdir}/xinetd.d,%{_sysconfdir}/%{name},/var/log/%{name}}
install -p build/apt-cacher-ng $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -p build/acngfs $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -p build/in.acng  $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -p expire-caller.pl distkill.pl $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -p doc/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -a conf/{*mirror*,*.html,*.css} $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a conf/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
cd $RPM_BUILD_ROOT%{_sysconfdir}/%{name} && cp -s ../..%{_libdir}/%{name}/{*mirror*,*.html,*.css} . && cd -
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO INSTALL*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xinetd.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man8/acngfs.8*
%{_mandir}/man8/apt-cacher-ng.8*
%dir /var/log/%{name}
