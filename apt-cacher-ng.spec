Summary:	Caching HTTP download proxy for software packages
Name:		apt-cacher-ng
Version:	0.3.8
Release:	0.1
License:	Public domain
Group:		Development
Source0:	http://ftp.debian.org/debian/pool/main/a/apt-cacher-ng/%{name}_%version.orig.tar.gz
# Source0-md5:	d0d4b168c4b814c5ddaa6a8410610f07
URL:		http://www.unix-ag.uni-kl.de/~bloch/acng/
BuildRequires:	boost-devel
#BuildRequires:	bzlib-devel
BuildRequires:	libfuse-devel
BuildRequires:	libstdc++-devel
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
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir} $RPM_BUILD_ROOT%{_libdir}/%{name} $RPM_BUILD_ROOT%{_mandir}/man8/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d
install -p apt-cacher-ng $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -p acngfs $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -p in.acng expire-caller.pl distkill.pl $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -p doc/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -a conf/{*mirror*,*.html,*.css} $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a conf/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
cd $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ && cp -s ../..%{_libdir}/%{name}/{*mirror*,*.html,*.css} . && cd -
install -d $RPM_BUILD_ROOT/var/log/%{name}/

cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/%{name}
# default: off
# description: The %{name} server.
service %{name}
{
	disable		= yes
	socket_type	= stream
	protocol	= tcp
	wait		= no
	user		= root
	nice		= 10
	rlimit_as	= 16M
	server		= %{_sbindir}/in.acng
	only_from	= 127.0.0.1
	server_args = -c %{_sysconfdir}/%{name}
}
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README TODO
%{_sysconfdir}/%{name}/
%{_sysconfdir}/xinetd.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%{_libdir}/%{name}/
%{_mandir}/man8/*
/var/log/%{name}/
