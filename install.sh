#!/bin/sh
# Desc: Create a FreeBSD service to run pfstalker.py as a daemon on pfSense firewall.
# Repo: https://github.com/usrbinbrain/pfstalker

TARGETSCRIPT=pfstalker.py
FULLPATHTARGET=${PWD}/${TARGETSCRIPT}
SERVICEPATH=/usr/local/etc/rc.d
SERVICENAME=${TARGETSCRIPT%%.*}
SERVICEFILE=${SERVICEPATH}/${SERVICENAME}
EXISTMSG="[!] Service ${SERVICENAME} exist in this host ( $(hostname):${SERVICEFILE} )."
INSTALLMSG="[+] Service (${SERVICENAME}) was installed on this host ( $(hostname) ).\n[!] Restart service with bellow command: service ${SERVICENAME} restart\n"
CANTINSTALLMSG="[-] Cant locate target script (${FULLPATHTARGET})."

# Verify if service is already installed.
[ -f "${SERVICEFILE}.sh" ] && echo "${EXISTMSG}" && exit ||
# Verify full path targert script.
[ ! -f "${FULLPATHTARGET}" ] && echo "${CANTINSTALLMSG}" && exit ||
# Create daemon service file.
cat > ${SERVICEFILE}.sh <<EOF
#!/bin/sh
. /etc/rc.subr
name=${SERVICENAME}
rcvar=${SERVICENAME}_enable
pidfile="/var/run/\${name}.pid"
logfile="/tmp/\${name}.log"
${SERVICENAME}_chdir="${PWD}"
script_command="${FULLPATHTARGET}"
command="/usr/sbin/daemon"
command_args="-P \${pidfile} -o \${logfile} -r -f \${script_command}"
load_rc_config \$name
run_rc_command "\$1"
EOF
# Enable file exec.
chmod +x ${FULLPATHTARGET} ${SERVICEFILE}.sh
# Enable service with sysrc.
sysrc -e "${SERVICENAME}_enable=YES"
# Create link to call service file.
ln -s ${SERVICEFILE}.sh ${SERVICEFILE}
# Show service information.
printf "${INSTALLMSG}"
