Summary:	Mail reader
Name:		cone
Version:	0.90
Release:	5
License:	GPLv2+
Group:		Networking/Mail
Url:		http://www.courier-mta.org/cone
Source0:	http://prdownloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2.sig
BuildRequires:	autoconf2.5
BuildRequires:	aspell-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig(gamin)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)

%description
CONE is a simple, text-based E-mail reader and writer.

%files
%doc ABOUT-NLS ChangeLog README NEWS AUTHORS COPYING* cone/html
%attr(644,root,root) %{_sysconfdir}/cone.dist
%ghost %attr(0644,root,root) %{_sysconfdir}/cone
%attr(0755,root,root) %{_bindir}/cone
%attr(0755,root,root) %{_bindir}/leaf
%attr(0755,root,root) %{_bindir}/mailtool
%attr(0755,root,root) %{_libexecdir}/cone
%{_datadir}/cone
%{_mandir}/man1/*

%preun
if [ "$1" = 0 ]; then
    mv %{_sysconfdir}/cone %{_sysconfdir}/cone.rpmsave
fi

%pre
if [ "$1" = 1 -a -f %{_sysconfdir}/cone.rpmsave -a ! -f %{_sysconfdir}/cone ]; then
    mv %{_sysconfdir}/cone.rpmsave %{_sysconfdir}/cone
fi

%post
perl %{_datadir}/cone/cone.sysconftool %{_sysconfdir}/cone.dist > /dev/null

#----------------------------------------------------------------------------

%package	devel
Summary:	LibMAIL mail client development library
Group:		Development/C++

%description	devel
The %{name}-devel package the header files and library files for
developing application using LibMAIL - a high level, C++ OO
library for mail clients.

%files devel
%{_libdir}/*.a
%{_mandir}/man[35]/*
%{_includedir}/libmail

#----------------------------------------------------------------------------

%prep
%setup -q

%build
export CC=gcc
export CXX=g++

%configure2_5x \
	--enable-shared \
	--enable-static \
	--enable-fast-install \
	--with-devel
%make

%install
%makeinstall_std
install sysconftool %{buildroot}%{_datadir}/cone/cone.sysconftool
touch %{buildroot}%{_sysconfdir}/cone

pushd %{buildroot}%{_datadir}/cone
    for i in *.html; do
	ln -snf ../doc/%{name}/html/$i $i
    done
popd

# install missing files
install -m755 libmail/mailtool %{buildroot}%{_bindir}/mailtool
install -m644 help.txt %{buildroot}%{_datadir}/cone/

