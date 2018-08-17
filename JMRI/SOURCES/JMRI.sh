#!/bin/bash
#
# Script to start a JMRI application.
#
# This script is used for all POSIX operating systems including Linux
#
# If you need to specify an option with spaces in it, escape the spaces with a
# leading backslash like "\ ".
#
# If you need to add any persistent Java options or persistent command line
# arguments, include them in the "default_options" statement in the file
# jmri.conf in the settings directory.
#
# The default location for the settings directory is: ${HOME}/.jmri
#
# The settings directory can be set to a non-standard location using the
# "--settingsdir=/path/to/my/settings" command line option (unlike all other
# options, this one cannot be set in the jmri.conf file, since it determines
# from where the jmri.conf file is read).
#
# If your serial ports are not in the default list, include them in the
# command line argument --serial-ports separated by commas:
#    --serial-ports=/dev/locobuffer,/dev/cmri
#
# You can run separate instances of the program with their own preferences
# if you
# - Provide the name of a configuration file as a parameter
# or
# - Copy and rename this script.
#
# If you rename the script to, for example, JmriNew, it will use
# "JmriNewConfig.properties" as it's configuration file. Note that configuration
# files only determine which profile to use, and if the profile selector should
# be shown at application launch.
#
# If you are getting X11 warnings about meta keys, uncomment the next line
# xprop -root -remove _MOTIF_DEFAULT_BINDINGS
#
# For more information, please see
# http://jmri.org/help/en/html/doc/Technical/StartUpScripts.shtml

# prevent the use of unbound variables
set -u

# display valid arguments
function usage() {
    cat <<EOM
Usage: $( basename $0 ) [--help] [OPTIONS] [--] [ARGUMENTS]
  -c CONFIG, --config=CONFIG     Start JMRI with configuration CONFIG
  --cp:a=CLASSPATH               Append specified JARs to the classpath
                                 Multiple JARs are separated with colons (:)
  --cp:p=CLASSPATH               Prepend specified JARs to the classpath
                                 Multiple JARs are separated with colons (:)
  -d, --debug                    Add verbose output to this script
  -DPROPERTY                     Set the Java System property PROPERTY
  -JOPTION                       Pass the option OPTION to the JVM
  -m MAIN, --main=MAIN           Use main() method in class MAIN to start JMRI
  -p PROFILE, --profile=PROFILE  Start JMRI with the profile PROFILE
  --serial-ports=SERIAL_PORTS    Use the serial ports in SERIAL_PORTS
  --settingsdir=SETTINGS_DIR     Use SETTINGS_DIR as the settings directory
  --                             Do not process anything following as an option,
                                 even if it matches one of the above options
EOM
}

# parse passed in arguments from either default_options or command line
# except --settingsdir argument
function parse_args() {
    while [ $# -gt 0 ] ; do
        if [ -z "${1}" ] ; then
            shift
            continue
        fi
        # note: set DEBUG=yes in environment to see at this point
        [ -n "${DEBUG}" ] && echo "Parsing Arg: '${1}'" | tee -a ${launcher_log}
        case "${1}" in
            # append to classpath
            --cp:a) post_classpath="${post_classpath}:${2}" ; shift ;;
            --cp:a=*) post_classpath="${post_classpath}:${1#*=}" ;;
            # prepend to classpath
            --cp:p) pre_classpath="${pre_classpath}:${2}" ; shift ;;
            --cp:p=*) pre_classpath="${pre_classpath}:${1#*=}" ;;
            # use named configuration
            -c|--config) CONFIGNAME="${2}" ; shift ;;
            --config=*) CONFIGNAME="${1#*=}" ;;
            # Java system properties
            -D*) jmri_options="${jmri_options} ${1}" ;;
            # debugging
            -d|--debug) DEBUG="yes" ;;
            # help
            --help) usage ; exit 2 ;;
            # heap sizes
            -J-Xms*) jmri_xms="${1#-J}" ;;
            -J-Xmx*) jmri_xmx="${1#-J}" ;;
            # JVM arguments other than max memory
            -J*) jmri_options="${jmri_options} ${1#-J}" ;;
            # main class
            -m|--main) CLASSNAME="${2}" ; shift ;;
            --main=*) CLASSNAME="${1#*=}" ;;
            # JMRI configuration profile
            -p|--profile) jmri_options="${jmri_options} -Dorg.jmri.profile=${2}" ; shift ;;
            --profile=*) jmri_options="${jmri_options} -Dorg.jmri.profile=${1#*=}" ;;
            # serial ports
            --serial-ports) JMRI_SERIAL_PORTS="${2}" ; shift ;;
            --serial-ports=*) JMRI_SERIAL_PORTS="${1#*=}" ;;
            # ignore and do not pass the settingsdir argument
            --settingsdir) shift ;;
            --settingsdir=*) ;;
            # ignore and do not pass a ProcessSerialNumber argument (from the open command on macOS)
            -psn_*) ;;
            # everything after this is to be passed to JMRI
            --) ARGS="${ARGS} $@" ; break ;;
            # pass anything else on to JMRI
            *) ARGS="${ARGS} ${1}" ;;
        esac
        shift
    done
}

# Get the default heap size for JMRI in MB.
# Based on total memory size, this is:
# - 1/4 total memory size on systems with more than 4GB RAM
# - 1/2 total memory size on systems with 1-4GB RAM
# - 3/4 total memory size on systems with less than 1GB RAM
# - with an absolute minimum of 192MB
function heap_size() {
    # get Java heap size
    heap=$( "${JAVACMD}" -XX:+PrintFlagsFinal -version 2>/dev/null | grep MaxHeapSize | awk '{print $4}' )
    heap=$( expr ${heap} / 1048576 ) # bytes to MB
    # Java heap defaults to 1/4 total memory size
    # if <= 768MB (1/4 of 3GB), set it ourselves
    if [ ${heap} -le 768 ] ; then
        mem=$( cat /proc/meminfo | grep MemTotal | tr -d [:space:][:alpha:]: )
        mem=$( expr $mem / 1024 )
       
        if [ -z "$mem" ] ; then
            mem=640
        fi
        if [ $mem -le 1024 ] ; then
          heap=$( expr $mem \* 3 / 4 )
        else
          heap=$( expr $mem \* 1 / 2 )
        fi
        if [ $heap -lt 192 ] ; then
            heap=192 # 3/4 of 256MB
        fi
    fi
    echo $heap
    return 0
}

# get the script's location as an absolute path
SCRIPTDIR=$(cd "$( dirname "${0}" )" && pwd)

# define the class to be invoked
APPNAME=$( basename "$0" )

case ${APPNAME} in
    DecoderPro)   CLASSNAME="apps.gui3.dp3.DecoderPro3" ;;
    InstallTest)  CLASSNAME="apps.InstallTest.InstallTest" ;;
    JmriFaceless) CLASSNAME="apps.JmriFaceless" ;;
    PanelPro)     CLASSNAME="apps.PanelPro.PanelPro" ;;
    SoundPro)     CLASSNAME="apps.SoundPro.SoundPro" ;;
    *)            CLASSNAME="apps.InstallTest.InstallTest"
                  echo "Using ${CLASSNAME} for ${APPNAME}" ;;
esac

# define empty jmri_options
jmri_options=""

# define empty array of passed in options
declare -a all_options=()

# ensure JMRI environment options are always set
JMRI_OPTIONS=${JMRI_OPTIONS:-}
JMRI_SERIAL_PORTS=${JMRI_SERIAL_PORTS:-}

# set default config name
CONFIGNAME=""
CONFIGFILE=""

# Installation locations
JAVA_HOME=${JAVA_HOME:-}
JMRI_HOME=${JMRI_HOME:-}
BUNDLEDIR=""

# Set default arguments
ARGS=

# set DEBUG to any non-empty string to see debugging output
DEBUG=${DEBUG:-}

# set default classpaths additions
pre_classpath=""
post_classpath=""

# set the OS (can be overridden in environment for debugging and development)
# this value is used to find OS-specific libraries, so it gets normalized
# in following case statement
OS=${OS:-}
if [ -z "${OS}" ] ; then
  OS=$( uname -s )
fi
ARCH=${ARCH:-}

# set OS-specific settings
case "${OS}" in
    Linux*)
        settingsdir="${HOME}/.jmri"
        OS="linux"
        ;;
    *)
        settingsdir="${HOME}/.jmri"
        ;;
esac

# get the settings directory if set on command line
found_settingsdir=""
for opt in "$@"; do
    if [ "${found_settingsdir}" = "yes" ]; then
        # --settingsdir /path/to/... part 2
        settingsdir="$opt"
        jmri_options="${jmri_options} -Djmri.prefsdir=${settingsdir}"
        break
    elif [ "$opt" = "--settingsdir" ]; then
        # --settingsdir /path/to/... part 1
        found_settingsdir="yes"
    elif [[ "$opt" =~ "--settingsdir=" ]]; then
        # --settingsdir=/path/to/...
        settingsdir="${opt#*=}"
        jmri_options="${jmri_options} -Djmri.prefsdir=${settingsdir}"
        break;
    fi
done

# log to $settingsdir/log/launcher.log for debugging purposes
launcher_log=${settingsdir}/log/launcher.log
mkdir -p ${settingsdir}/log
[ -f ${launcher_log} ] && rm -f ${launcher_log}

# process arguments, stored arguments first, so CLI arguments can override

# process default_options from the launcher configuration file
if [ -f "${settingsdir}/jmri.conf" ] ; then
    default_options=""
    source "${settingsdir}/jmri.conf"
    if [ -n "${default_options}" ] ; then
        IFS=' ' read -a all_options <<< "${default_options}"
    fi
fi

# process environment and command line arguments
if [ -n "${JMRI_OPTIONS}" ] ; then
    IFS=' ' read -a options <<< "${JMRI_OPTIONS}"
    for option in "${options[@]}" ; do
        all_options=("${all_options[@]-}" "${option}")
    done
fi
if [ $# -gt 0 ] ; then
    for option in "$@"; do
        all_options=("${all_options[@]-}" "${option}")
    done
fi
parse_args "${all_options[@]:-}"

# define JAVA_HOME if needed
if [ -z "${JAVA_HOME}" ] ; then
    if which java >/dev/null 2>&1 ; then
        JAVACMD=$( which java )
        JAVA_HOME="$( dirname ${JAVACMD} )/.."
    else
        echo "Please install Java 1.8 per your operating system vendor's instructions." | tee -a ${launcher_log}
        exit 1
    fi
else
    JAVACMD="${JAVA_HOME}/bin/java"
    if [ ! -x "${JAVACMD}" ] ; then
        echo "Unable to execute java using JAVA_HOME=\"${JAVA_HOME}\"." | tee -a ${launcher_log}
        exit 1
    fi
fi
# make JAVA_HOME available to spawned processes
export JAVA_HOME

# set if -J-Xmx=... is not in options or arguments
if [ -z "${jmri_xmx:-}" ] ; then
    jmri_xmx="-Xmx$( heap_size )m"
fi
# set if -J-Xms=... is not in options or arguments
if [ -z "${jmri_xms:-}" ] ; then
    # initial heap size = default for 6 GB RAM (default = 1/64 installed RAM)
    jmri_xms="-Xms96m"
fi

# permit Java 9 illegal access
if [[ $( "${JAVACMD}" -version 2>&1 | grep version ) =~ \"9 ]] ; then
    jmri_options="${jmri_options} --illegal-access=warn"
fi

# define JMRI_HOME if it is not defined
if [ -z "${JMRI_HOME}" ] ; then
    JMRI_HOME="${SCRIPTDIR}/../share/JMRI"
fi

cd "${JMRI_HOME}"
[ -n "${DEBUG}" ] && echo "PWD: '${PWD}'" | tee -a ${launcher_log}



# build classpath dynamically
CP=""
if [ -n "${pre_classpath}" ] ; then
    pre_classpath="${pre_classpath#:}"
    CP="${pre_classpath}:"
fi

CP="${CP}:$(build-classpath org.jmri:jmri)"

# Direct dependencies
CP="${CP}:$(build-classpath \
   com.digi.xbee:xbjlib \
   com.fasterxml.jackson.core:jackson-annotations \
   com.fasterxml.jackson.core:jackson-core \
   com.fasterxml.jackson.core:jackson-databind \
   com.google.code.findbugs:annotations \
   com.google.code.findbugs:jsr305 \
   com.google.guava:guava \
   com.networknt:json-schema-validator \
   com.sparetimelabs:purejavacomm \
   commons-io:commons-io \
   javax.help:javahelp \
   javax.mail:javax.mail-api \
   javax.servlet:javax.servlet-api \
   javax.usb:usb-api \
   javax.vecmath:vecmath \
   log4j:log4j:12 \
   net.java.dev.jna:jna-platform \
   net.java.dev.jna:jna \
   net.java.jinput:jinput \
   net.java.jutils:jutils \
   net.jcip:jcip-annotations \
   net.sf.bluecove:bluecove \
   net.sourceforge.javacsv:javacsv \
   org.apache.commons:commons-lang3 \
   org.apache.commons:commons-text \
   org.eclipse.jetty.websocket:websocket-api \
   org.eclipse.jetty.websocket:websocket-client \
   org.eclipse.jetty.websocket:websocket-common \
   org.eclipse.jetty.websocket:websocket-server \
   org.eclipse.jetty.websocket:websocket-servlet \
   org.eclipse.jetty:jetty-client \
   org.eclipse.jetty:jetty-http \
   org.eclipse.jetty:jetty-io \
   org.eclipse.jetty:jetty-security \
   org.eclipse.jetty:jetty-server \
   org.eclipse.jetty:jetty-servlet \
   org.eclipse.jetty:jetty-util\
   org.eclipse.jetty:jetty-xml \
   org.eclipse.paho:org.eclipse.paho.client.mqttv3 \
   org.hid4java:hid4java \
   org.jdesktop:beansbinding \
   org.jdom:jdom2 \
   org.jmdns:jmdns \
   org.jogamp.gluegen:gluegen-rt \
   org.jogamp.joal:joal \
   org.netbeans.api:org-openide-util-lookup \
   org.openlcb:openlcb \
   org.python:jython-standalone \
   org.slf4j:jul-to-slf4j \
   org.slf4j:slf4j-api \
   org.slf4j:slf4j-ext \
   org.slf4j:slf4j-log4j12 \
   org.usb4java:libusb4java \
   org.usb4java:usb4java-javax \
   org.usb4java:usb4java \
   xerces:xercesImpl \
   xml-apis:xml-apis \
)"

# Jython dependencies
CP="${CP}:$(build-classpath \
   com.github.jnr:jffi \
   com.github.jnr:jffi::native: \
   com.github.jnr:jnr-constants \
   com.github.jnr:jnr-ffi \
   com.github.jnr:jnr-netdb \
   com.github.jnr:jnr-posix \
   com.google.guava:guava \
   com.ibm.icu:icu4j \
   io.netty:netty-buffer \
   io.netty:netty-codec \
   io.netty:netty-common \
   io.netty:netty-handler \
   io.netty:netty-resolver \
   io.netty:netty-transport \
   jline:jline \
   org.antlr:antlr-runtime:3.2 \
   org.apache.commons:commons-compress \
   org.bouncycastle:bcpkix-jdk15on \
   org.bouncycastle:bcprov-jdk15on \
   org.fusesource.jansi:jansi \
   org.jctools:jctools-core \
   org.ow2.asm:asm-commons \
   org.ow2.asm:asm \
   org.ow2.asm:asm-util \
)"

if [ -n "${post_classpath}" ] ; then
    post_classpath="${post_classpath#:}"
    CP="${CP}:${post_classpath}"
fi

# remove any "\ " escaped spaces, since these are needed for bash, but not java
CP="${CP//\\ / }"

[ -n "${DEBUG}" ] && echo "CLASSPATH: '${CP}'" | tee -a ${launcher_log}

[ -n "${DEBUG}" ] && echo "Java CMD: '${JAVACMD[@]}'" | tee -a ${launcher_log}

# configuration file name is 1st argument.
# If not provided, build config file name dynamically
#APPNAME=$( basename "$0" )

[ -n "${DEBUG}" ] && echo "APPNAME: '${APPNAME}'" | tee -a ${launcher_log}
[ -n "${DEBUG}" ] && echo "CLASSNAME: '${CLASSNAME}'" | tee -a ${launcher_log}

# Process a config file name if passed as an option and pass it as a
# Java property so that scripts expecting another argument as the
# first one get that instead
if [ -n "${CONFIGNAME}" ] ; then
    CONFIGFILE="-Dorg.jmri.Apps.configFilename=${CONFIGNAME}Config.xml"
    [ -n "${DEBUG}" ] && echo "CONFIGFILE: '${CONFIGFILE}'" | tee -a ${launcher_log}
fi

# create the option string
#
# Add JVM and RMI options to user options, if any

OPTIONS="${jmri_options} -noverify"
OPTIONS="${OPTIONS} -Djava.security.policy=${JMRI_HOME}/security.policy"
#OPTIONS="${OPTIONS} -Djava.rmi.server.codebase=file:target/classes/"
#OPTIONS="${OPTIONS} -Djava.library.path=.:/usr/share/java:/usr/lib/java"

# memory start and max limits
OPTIONS="${OPTIONS} ${OS_OPTIONS-} ${jmri_xms} ${jmri_xmx}"
[ -n "${DEBUG}" ] && echo "OPTIONS: '${OPTIONS}'" | tee -a ${launcher_log}

# handle ports in --settings argument or JMRI_SERIAL_PORTS environment variable
# but not if already in OPTIONS
ALTPORTS=
if [[ -n "${JMRI_SERIAL_PORTS}" && ! ${OPTIONS} =~ "-Dpurejavacomm.portnamepattern=" ]] ; then
    ALTPORTS="-Dpurejavacomm.portnamepattern=${JMRI_SERIAL_PORTS}"
fi


RESTART_CODE=100
EXIT_STATUS=${RESTART_CODE}
while [ "${EXIT_STATUS}" -eq "${RESTART_CODE}" ] ; do
    "${JAVACMD}" ${OPTIONS} ${ALTPORTS} ${CONFIGFILE} -cp "${CP}" "${CLASSNAME}" ${ARGS}

    EXIT_STATUS=$?
    [ -n "${DEBUG}" ] && echo Exit Status: "${EXIT_STATUS}" | tee -a ${launcher_log}
done

exit $EXIT_STATUS
