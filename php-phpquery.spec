%define		pkgname	phpQuery
%define		php_min_version 5.2.0
Summary:	phpQuery - jQuery port to PHP
Name:		php-phpquery
Version:	0.9.5.386
Release:	0.13
License:	The MIT License
Group:		Development/Languages/PHP
Source0:	https://phpquery.googlecode.com/files/phpQuery-%{version}.zip
# Source0-md5:	3ddab515c82a1a102a87f90ab319e7d1
Patch0:		svn.patch
Patch1:		sys-mbstring.patch
Patch2:		cli.patch
URL:		https://code.google.com/p/phpquery/
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.610
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(dom)
Requires:	php(json)
Requires:	php(mbstring)
Requires:	php(pcre)
Requires:	php-pear
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# bad depsolver
%define		_noautopear	pear(phpQuery.php/phpQuery/.*) pear(phpQuery/plugins/Scripts/__config.php)

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
phpQuery is a server-side, chainable, CSS3 selector driven Document
Object Model (DOM) API based on jQuery JavaScript Library.

%prep
%setup -qc
mv phpQuery .pq; mv .pq/* .
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

# fix shebang
%{__sed} -i -e '1s,^#!.*env php,#!/usr/bin/php,' cli/phpquery

# use ext
rm %{pkgname}/%{pkgname}/compat/mbstring.php
rmdir %{pkgname}/%{pkgname}/compat

# use Zend packages directly
mv %{pkgname}/%{pkgname}/Zend .

# separate examples
install -d examples/plugins/Scripts
mv %{pkgname}/%{pkgname}/bootstrap.example.php examples
mv %{pkgname}/%{pkgname}/plugins/Scripts/*example.php examples/plugins/Scripts
mv %{pkgname}/%{pkgname}/plugins/*example.php examples/plugins
mv demo.php examples

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_data_dir}/%{pkgname},%{_bindir},%{_examplesdir}/%{name}-%{version}}

cp -a %{pkgname}/* $RPM_BUILD_ROOT%{php_data_dir}
install -p cli/phpquery $RPM_BUILD_ROOT%{_bindir}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/phpquery
%{php_data_dir}/phpQuery.php
%{php_data_dir}/phpQuery
%{_examplesdir}/%{name}-%{version}
