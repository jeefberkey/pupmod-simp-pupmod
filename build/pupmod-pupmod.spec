Summary: Puppet Management Puppet Module
Name: pupmod-pupmod
Version: 6.0.1
Release: 24
License: Apache License, Version 2.0
Group: Applications/System
Source: %{name}-%{version}-%{release}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: hiera >= 1.3.0
Requires: pupmod-apache >= 4.1.0-1
Requires: pupmod-simpcat >= 4.0.0-0
Requires: pupmod-iptables >= 4.1.0-3
Requires: pupmod-puppetlabs-inifile >= 1.0.0
Requires: puppet >= 3.3.0
Requires: puppetlabs-stdlib >= 4.1.0
Requires: pupmod-augeasproviders_grub >= 1.0.2
Requires: pupmod-augeasproviders_puppet >= 1.0.2
Buildarch: noarch
Requires: simp-bootstrap >= 4.2.0
Obsoletes: pupmod-pupmod-test >= 0.0.1
Requires: pupmod-onyxpoint-compliance_markup

Prefix: %{_sysconfdir}/puppet/environments/simp/modules

%description
This unfortunately named Puppet module provides the capability to configure both
puppet servers and puppet clients.

The ability to switch puppetd from a system service to a cron job is also
supported.

%prep
%setup -q

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/%{prefix}/pupmod

dirs='files lib manifests templates'
for dir in $dirs; do
  test -d $dir && cp -r $dir %{buildroot}/%{prefix}/pupmod
done

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/%{prefix}/pupmod

%files
%defattr(0640,root,puppet,0750)
%{prefix}/pupmod

%post
#!/bin/sh

%postun
# Post uninstall stuff

%changelog
* Thu May 19 2016 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.1-0
- Made master::reports a private class

* Thu Feb 25 2016 Ralph Wright <ralph.wright@onyxpoint.com> - 6.0.0-24
- Added compliance function support

* Wed Feb 24 2016 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-24
- Fix the subscribe on the Service['puppet'] resource to not be a hard coded
  path.

* Thu Dec 24 2015 Trevor Vaughan <tvaughahn@onyxpoint.com> - 6.0.0-23
- Fixed minor logic errors
- Now have configuration changes notify Service['puppetserver'] instead of the
  more efficient Exec. This gets around a race condition when the service is
  restarted and the exec fires before the service has fully restarted.
- Fixed issues with the puppetserver_* helper scripts that surfaced due to
  changes in the HTTP responses from the Puppet Server.

* Fri Dec 04 2015 Chris Tessmer <chris.tessmer@onyxpoint.com> - 6.0.0-22
- Replaced all 'lsb*' facts with their (package-independent)
  'operatingsystem*' counterparts.
- Moved parameter validations to the top of each class.

* Mon Nov 09 2015 Chris Tessmer <chris.tessmer@onyxpoint.com> - 6.0.0-21
- migration to simplib and simpcat (lib/ only)

* Wed Nov 04 2015 Chris Tessmer <chris.tessmer@onyxpoint.com> - 6.0.0-20
- Improved logic for  defaults

* Thu Sep 17 2015 Kendall Moore <kmoore@keywcorp.com> - 6.0.0-19
- Ensure keylength is set to 2048 in puppet.conf if FIPS mode is enabled.

* Wed Jun 17 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-18
- Remove the legacy code that restarted httpd when the Puppet CRL was
  downloaded.

* Tue May 05 2015 Jacob Gingrich <jacob.gingrich@onyxpoint.com> - 6.0.0-17
- Enabled the puppetserver service

* Fri Mar 20 2015 Kendall Moore <kmoore@keywcorp.com> - 6.0.0-16
- Added a puppet_ruby_dir fact to return the location of the
  runtime ruby directory for Puppet on the client.

* Wed Feb 18 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-16
- Updated to use the refactored Augeasproviders

* Fri Jan 16 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-15
- Changed puppet-server requirement to puppet
- Added full support for the new Clojure-based Puppet Server
- Removed all support for the Passenger Puppet Master

* Wed Dec 03 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-14
- Changed 'splay' to false
- Properly handles true/false values in the puppet conf settings.
- Added support for $runinterval, $splaylimit, and $configtimeout
- Added full class validation
- Multiple fixes to the cron script:
  - No longer uses values from the Puppet master to make decisions.
  - Properly differentiates between the run lock file and the manual
    disabling of the system.

* Tue Nov 25 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-13
- Updated the agent cron job to be able to use alternate run intervals
  as well as support an alternate base for run randomization. This
  means that you can use something *other* than IP address to
  randomize your nodes. Any string will work.

* Fri Oct 17 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-12
- CVE-2014-3566: Updated protocols to mitigate POODLE.

* Mon Sep 08 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-11
- Add appropriate confines to the passenger* facts and no longer hard
  code paths.
- Ensure that the puppetmaster init does not fire off alongside httpd.
- Made the change for puppet_manage_all_files conditional on the
  RHEL/CentOS version since this needs to work on both 6 and 7.

* Wed Aug 27 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-10
- Changed the $passenger_temp_dir selinux type from tmp_t to
  httpd_var_run_t since it is now in /var/run/passenger by default.

* Tue Aug 26 2014 Kendall Moore <kmoore@keywcorp.com> - 6.0.0-9
- Updated the passenger_version fact to return "unknown" when Passenger is not installed.

* Mon Aug 25 2014 Kendall Moore <kmoore@keywcorp.com> - 6.0.0-9
- SELinux boolean puppet_manage_all_files was changed to puppetagent_manage_all_files.

* Mon Jul 14 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-8
- Updated the code to only enable the puppetmaster init script if passenger is
  not enabled and the init system includes systemd.
- Added a setitng to set 'stringify_facts' to 'false' in the [main]
  section of puppet.conf. This was not made a variable since complex
  facts in other parts of the system will fail without it.

* Tue Jul 01 2014 Adam Yohrling <adam.yohrling@onyxpoint.com> - 6.0.0-7
- Added puppet_auth type to make sure puppet master is able to access
  node REST endpoint for puppetlast script to work
- Added pupmod RPM requirement of pupmod-augeasproviders

* Mon Jun 23 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-6
- Added a segment for using a passenger service stub to ensure that the
  passenger service can properly run.
- Fixed a bug in the passenger template for apache where the output
  configuration would be incorrect should you have both the master and
  CA ports identically set.
- Fixed SELinux check for when selinux_current_mode is not found.

* Sun Jun 22 2014 Kendall Moore <kmoore@keywcorp.com> - 6.0.0-6
- Removed MD5 file checksums for FIPS compliance.
- Updated puppet conf to set the digest algorithm to SHA-256 by default.

* Fri Jun 13 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-5
- Updated the code to use environment directories instead of the
  'manifest' option since it is deprecated in Puppet 3.6.

* Fri May 16 2014 Kendall Moore <kmoore@keywcorp.com> - 6.0.0-4
- Updated the passenger manifest to convert the SSL cipher suite to an array
  and updated the passenger template to correspond to this change.

* Sun Apr 20 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-3
- master::freeze_main is now set to true by default.
- Changed back to /bin/logger since that is correct for RHEL/CentOS 6

* Wed Apr 16 2014 Nick Markowski <nmarkowski@keywcorp.com> - 6.0.0-2
- Selinux booleans now set if mode != disabled
- Fixed some minor errors in rspec tests, and updated them for the
  Selinux change.
- Updated facter value calls to new standard

* Fri Apr 04 2014 Nick Markowski <nmarkowski@keywcorp.com> - 6.0.0-2
- Selinux booleans now set if mode != disabled
- Fixed some minor errors in rspec tests, and updated them for the
  Selinux change.

* Fri Mar 28 2014 Kendall Moore <kmoore@keywcorp.com> - 6.0.0-1
- Updated puppetagent_cron script to ignore output when stopping the puppet service.

* Wed Feb 12 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-0
- Converted all string booleans to booleans.
- Refactored the entire module to use puppetlabs-inifile for
  puppet.conf management.
- Parameterized as many variables as reasonable in the classes to
  allow for flexibility.
- Added a CRL downloading cron job to update the Puppet CRLs on all
  hosts on a regular basis.
- Updated the puppetmaster init script to ignore mongrel settings and
  reload apache properly on update.
- Added a requirement on puppetlabs-inifile to manage only specific
  entries in puppet.conf.
- This should not break any existing installations but will not
  trap, nor manage, by default all of the values that were previously
  specified.
- A new define pupmod::conf has been added to provide for the
  manipulation of configuration file entries.
- Added basic puppet-rspec tests.
- Set SSLVerifyClient to optional for CA

* Mon Oct 07 2013 Kendall Moore <kmoore@keywcorp.com> - 5.0.0-2
- Updated all erb templates to properly scope variables.

* Tue Oct 01 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.0.0-1
- Fixed change to pupmod::passenger::add_site which changed the name of the
  site and, therefore, the name of the file in /etc/httpd/conf.d. This caused a
  conflict on upgrade.

* Tue Sep 24 2013 Kendall Moore <kmoore@keywcorp.com> - 5.0.0-0
- Require puppet 3.X and puppet-server 3.X because of an upgrade to use
  hiera instead of extdata.
- Updated the config.ru and apache_passenger templates as well as the passenger::add_site
  manifest to support new passenger options in Puppet 3.1.
- Updated puppetagent_cron template by changing lockfile variable according to Puppet 3.

* Tue Sep 24 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.2.0-5
- Moved the passenger temp directory from /tmp to /var/run/passenger.
  The permissions on the socket files were simply too permissive to
  have hanging about in /tmp. Puppetmaster_switch and the init script
  were updated to accommodate the change.

* Thu Aug 15 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.2.0-4
- Re-introduced the passenger_root fact but made it more intelligent.
- Set the passenger_root variable to $::passenger_root by default.

* Thu Jun 13 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.2.0-3
- Added audit rules that will watch the /etc/puppet directory tree for writes
  or attribute changes not performed by the puppet user.

* Tue Feb 05 2013 Kendall Moore <kmoore@keywcorp.com> - 4.2.0-2
- Created Cucumber tests to check basic puppet server and client features

* Tue Jan 29 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.2.0-1
- Added +ExportCertData to SSLOptions.

* Mon Dec 10 2012 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.2.0-0
- Updated the apache_passenger template to support most of the passenger
  options.
- Attempt to keep half as many puppetmaster instances running as are specified
  or calculated at all times. This should make response time better overall.
- Removed the passenger_root fact since the EPEL version of passenger doesn't
  supply the utils.
- This is another mid-level jump due to the fact that EPEL split out
  the native Passenger libraries! These are included in the associated
  patch set but there's no good way to tie them together explicitly so
  be careful!

* Wed Nov 28 2012 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-0
- Critical update to fix an issue where unowned files at the root level were
  getting recursively chowned to puppet.puppet.
- Moved all of the singleton defines to classes which will cause some files in
  simp-bootstrap to be reconfigured.

* Thu Jul 05 2012 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.0.0-5
- Fixed a typo where we had 'dbpasword' instead of 'dbpassword' for
  the server configuration.
- Updated the server and client configuration files with the options
  for the latest version.

* Thu Jun 07 2012 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.0.0-4
- Ensure that Arrays in templates are flattened.
- Call facts as instance variables.
- Optimized the find command for 'gem_permissions'.
- Moved mit-tests to /usr/share/simp...
- Updated pp files to better meet Puppet's recommended style guide.

* Fri Mar 02 2012 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.0.0-3
- Removed puppetd cron job from running systems since it conflicted with the
  new puppetagent cron job.
- Improved test stubs.

* Tue Jan 31 2012 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.0.0-2
- Remove newserver.erb, this fact is no longer required.

* Mon Dec 26 2011 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.0.0-1
- Updated the spec file to not require a separate file list.
- Scoped all of the top level variables.

* Mon Nov 14 2011 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.0.0-0
- Updated to ensure that the puppet cron using /usr/bin/logger instead of /bin/logger.

* Mon Oct 10 2011 Trevor Vaughan <tvaughan@onyxpoint.com> - 2.0.0-3
- Updated to put quotes around everything that need it in a comparison
  statement so that puppet > 2.5 doesn't explode with an undef error.

* Tue Aug 09 2011 Trevor Vaughan <tvaughan@onyxpoint.com> - 2.0.0-2
- Ensure that autosign.conf is 644.

* Mon Apr 18 2011 Trevor Vaughan <tvaughan@onyxpoint.com> - 2.0.0-1
- Update the puppet cron job to properly unlock. This was broken in previous
  releases. This feature is important in the case that puppet dies unexpectedly
  and leaves a lock file behind. The default is set to 4 times the croninterval
  and will not exceed 4 hours.
- Ensure that Passenger and Mongrel configuration files are not in the Apache
  space if attempting to run under a Mongrel server. Users should now have the
  ability to seamlessly switch between all three types of servers.
- Updated puppetmaster_switch exec to properly require files and only run if it
  has changed.
- Ensure that mongrel and passenger can switch between each other effectively.
- Changed all instances of defined(Class['foo']) to defined('foo') per the
  directions from the Puppet mailing list.
- Updated to use concat_build and concat_fragment types.

* Mon Apr 18 2011 Morgan Haskel <morgan.haskel@onyxpoint.com> - 2.0.0-1
- Changed puppet://$puppet_server/ to puppet:///
- Added two stock classes, cluster_client and cluster_master, for enabling NFS
  to help cluster puppet servers.

* Tue Jan 11 2011 Trevor Vaughan <tvaughan@onyxpoint.com> - 2.0.0-0
- Refactored for SIMP-2.0.0-alpha release
- Puppet.conf updated to deal with puppet deprecations
- svckill.rb added to puppet.conf postrun_command
- 'puppet' uid/gid changed to 52

* Tue Oct 26 2010 Maintenance - 1-5
- Converting all spec files to check for directories prior to copy.

* Tue Aug 03 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 1.0-4
- Updated puppetmaster init script to work with passenger.

* Thu Jul 22 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 1.0-3
- Removed all instances of 'daemonize' from templates as this caused horrible
  problems with activerecord.

* Thu Jul 01 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 1.0-2
- Updated puppetmaster_switch to work with external CA.
- Updated the configuration for Passenger to properly utilize CRLs.
- Added the ability for Passenger to listen on both 8140 and 8141 by default
  for legacy purposes.

* Thu Jul 01 2010 Morgan Haskel <morgan.haskel@onyxpoint.com> - 1.0-2
- Added templates needed for clustered puppetmasters.

* Wed Jun 16 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 1.0-1
- Added a fact that determines the passenger root directory if passenger is installed.

* Thu Jun 03 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 1.0-0
- Made server permissions changes less aggressive.

* Tue May 25 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 0.1-40
- Updated Passenger.

* Mon May 03 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 0.1-39
- Modified gem package names for Mongrel.

* Tue Apr 27 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 0.1-38
- Added the ability to set the 'certname' option in pupmod::client::main_conf

* Wed Mar 17 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 0.1-37
- Added the --no-splay option to the puppet runs in puppetmaster_switch.sh. This
  massively speeds things up if you have to re-run it later for some reason.

* Tue Feb 23 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 0.1-36
- Removed the 'nice' ability added in 0.1-33 as it propogates the nice value to
  all spawned services.

* Wed Feb 17 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 0.1-35
- Refactored the code to be more maintainable.
- Added the variables:
  $cronminute
  $cronhour
  $cronmonthday
  $cronmonth
  $cronweekday

  to pupmod::client::client_conf to allow users to set their own complete cron
  schedule for puppet runs. $croninterval still works but will be overridden if
  you set $cronminute to anything other than 'nil'.

* Thu Jan 28 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 0.1-33
- Added the ability to 'nice' the puppet cron job. The default 'nice' value is
  now '1'.

* Thu Jan 14 2010 Trevor Vaughan <tvaughan@onyxpoint.com> - 0.1-32
- Fixed typo in puppetd.cron in if comparison. Ignoring the override will now
  function properly.

* Thu Dec 31 2009 Trevor Vaughan <tvaughan@onyxpoint.com> - 0.1-31
- Fixed puppetmaster_switch.sh.  All instances of --no-show-diff have been
  changed to --no-show_diff.

* Thu Nov 05 2009 Trevor Vaughan <tvaughan@onyxpoint.com> - 0.1-30
- Prevent the puppetmaster_switch.sh script from printing diff information to
  the logs.
