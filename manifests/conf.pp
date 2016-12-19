# This is a simple define to call the Puppet INIFile class for the passed
# parameters on the puppet.conf file.
#
# The main purpose is to easily allow for a service trigger.
#
# @param name
#   A globally unique name for this resource. Will be prefixed with $modname
#
# @param setting
#   The setting in the section to set
#
# @param value
#   The value of the setting to be set.
#
# @param section
#   The Sections of the puppet.conf to set.
#
# @author Trevor Vaughan <tvaughan@onyxpoint.com>
#
define pupmod::conf (
  String $setting,
  Scalar $value,
  String $section = 'main'
) {
  include '::pupmod'

  $l_name = "${module_name}_${name}"

  ini_setting { $l_name:
    path    => "${::pupmod::confdir}/puppet.conf",
    section => $section,
    setting => $setting,
    # This needs to be a string to take effect!
    value   => $value
  }
}
