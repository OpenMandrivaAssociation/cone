Summary:	CONE mail reader
Name:		cone
Version:	0.74
Release:	%mkrel 1
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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# do not make this spec file as messy as courier-imap...
rm -f %{buildroot}%{_bindir}/cone
mv %{buildroot}%{_libdir}/cone %{buildroot}%{_bindir}/
mv %{buildroot}%{_sysconfdir}/cone.dist %{buildroot}%{_sysconfdir}/cone

# do not install the docs twice...
pushd %{buildroot}%{_datadir}/cone
    for i in *.html; do
	ln -snf ../doc/%{name}-%{version}/html/$i $i
    done
popd

# install missing files
install -m755 libmail/mailtool %{buildroot}%{_bindir}/mailtool
install -m644 help.txt %{buildroot}%{_datadir}/cone/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ABOUT-NLS ChangeLog README NEWS AUTHORS COPYING* cone/html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cone
%attr(0755,root,root) %{_bindir}/cone
%attr(0755,root,root) %{_bindir}/leaf
%attr(0755,root,root) %{_bindir}/mailtool
%{_datadir}/cone
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_mandir}/man[35]/*
%{_includedir}/libmail
