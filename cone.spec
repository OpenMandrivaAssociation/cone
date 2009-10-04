Summary:	CONE mail reader
Name:		cone
Version:	0.77
Release:	%mkrel 4
License:	GPL
Group:		Networking/Mail
URL:		http://www.courier-mta.org/cone
Source0:	http://prdownloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2.sig
BuildRequires:	aspell-devel
BuildRequires:	autoconf2.5
BuildRequires:	fam-devel
BuildRequires:	gcc-c++
BuildRequires:	ncurses-devel
BuildRequires:	libncursesw-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	perl
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
CONE is a simple, text-based E-mail reader and writer.

%package	devel
Group:		Development/C++
Summary:	LibMAIL mail client development library
Requires:	%{name}

%description	devel
The %{name}-devel package the header files and library files for
developing application using LibMAIL - a high level, C++ OO
library for mail clients.

%prep

%setup -q

%build

%configure2_5x \
    --enable-shared \
    --enable-static \
    --enable-fast-install \
    --with-devel

# these messes everything up real bad...
#    --datadir=%{_datadir}/cone \
#    --with-filterdir=%{_datadir}/cone/filters \
#    --with-certdb=%{_datadir}/cone/rootcerts \
#    --libexec=%{_bindir} \
#    --enable-mimetypes=%{_sysconfdir}/mime.types \

%make

%install
rm -rf %{buildroot}

%makeinstall_std

%{__install} sysconftool %{buildroot}%{_datadir}/cone/cone.sysconftool
touch %{buildroot}%{_sysconfdir}/cone

# do not install the docs twice...
pushd %{buildroot}%{_datadir}/cone
    for i in *.html; do
	ln -snf ../doc/%{name}/html/$i $i
    done
popd

# install missing files
install -m755 libmail/mailtool %{buildroot}%{_bindir}/mailtool
install -m644 help.txt %{buildroot}%{_datadir}/cone/

%preun
if [ "$1" = 0 ]; then
    mv %{_sysconfdir}/cone %{_sysconfdir}/cone.rpmsave
fi

%pre
if [ "$1" = 1 -a -f %{_sysconfdir}/cone.rpmsave -a ! -f %{_sysconfdir}/cone ]; then
    mv %{_sysconfdir}/cone.rpmsave %{_sysconfdir}/cone
fi

%post
%{__perl} %{_datadir}/cone/cone.sysconftool %{_sysconfdir}/cone.dist > /dev/null

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ABOUT-NLS ChangeLog README NEWS AUTHORS COPYING* cone/html
%attr(644,root,root) %{_sysconfdir}/cone.dist
%ghost %attr(0644,root,root) %{_sysconfdir}/cone
%attr(0755,root,root) %{_bindir}/cone
%attr(0755,root,root) %{_bindir}/leaf
%attr(0755,root,root) %{_bindir}/mailtool
%attr(0755,root,root) %{_libdir}/cone
%{_datadir}/cone
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_mandir}/man[35]/*
%{_includedir}/libmail
