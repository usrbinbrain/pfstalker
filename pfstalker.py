#!/usr/local/bin/python3.7

import re
import time
import json
import subprocess as sb

# Verify admin hash password.
def vrf_admin_hash(check_hash):
    """ Detect changes on admin user hash passord. """

    # Get admin hash on master.passwd file.
    with open("/etc/master.passwd", "r") as hash_file:
        hash_file = hash_file.read()
        admin_hash = re.findall(r"^admin\:(.*)\:\d\:\d\:\:", hash_file, re.MULTILINE)[0]

    # If None return current hash.
    if check_hash == None:

        return admin_hash

    else:

        # Verify change in hash.
        if check_hash != admin_hash:

            return None

        # If ok return hash.
        else:

            return admin_hash


# Verify SSH auth key.
def vrf_ssh_key(config):
    """ Deploy, verify and rollback SSH public key. """

    # SSH admin authorired keys full path.
    auth_keys = "/root/.ssh/authorized_keys"

    # Set SSH public key.
    ssh_key = config["ssh_public_key"][0]

    # Try read authorized key file.
    try:
        with open(auth_keys) as keys_file:
            keys_file = keys_file.read()

        # If SSH public key not exist in auth file, perform key rollback and return False.
        if ssh_key not in keys_file:
            with open(auth_keys) as keys_file:
                keys_file.write(f'{ssh_key}\n')

            return False

        # If key exist in auth keys file return True.
        else:
            return True

    # If auth keys file dont exist, just deploy public key on authorized_keys file and return None.
    except:
        with open(auth_keys, "w") as keys_file:
            keys_file.write(f'{ssh_key}\n')

        return False


# Verify SSH service status.
def vrf_ssh_service():
    """ Verify SSH service status and perform restart if daemon down. """

    # Try read SSH pid file.
    try:
        with open("/var/run/sshd.pid", "r") as sshd_id:
            sshd_id = sshd_id.read()

        return True

    # If file dont exist, check SSH service status and perform restart if service is not running.
    except:
        sshd_status = sb.getoutput("service sshd onestatus")
        if "sshd is not" in sshd_status:
            sb.getoutput("/usr/local/sbin/pfSsh.php playback enablesshd")

            return False


# Get localhost information.
def localhost_info():
    """ Get FreeBSD (pfSense) curl full path, hostname and default IPv4. """

    # Get hostname.
    fw_name = sb.getoutput('hostname')

    # Get curl full path.
    fp_curl = sb.getoutput('which curl')

    # Get default firewall NIC.
    fw_nic = sb.getoutput('netstat -rn4')
    fw_nic = re.findall(r"^default.*\s(\w+$)", fw_nic, re.MULTILINE)[0]

    # Get IPv4 on default firewall NIC.
    nic_ip = sb.getoutput(f'ifconfig {fw_nic} inet')
    nic_ip = re.findall(r"(.*inet\s)(.*)\s[:alfanum:]", nic_ip)[0][1]


    nic_ip = "10.10.10.254"

    # Return IPv4, hostname and curl full path.
    return {"ipv4": nic_ip, "name": fw_name, "curl": fp_curl}


# Discord sender.
def send_discord(alert_msg, local_info, config):
    """ Revice string 'alert_msg', object 'local_info' and send alert through curl to Discord webhook. """

    # Set localhost information.
    hostname = local_info["name"]
    ipv4 = local_info["ipv4"]
    curl = local_info["curl"]

    # Set webhook url.
    discord_webhook = config["webhooks_config"]["discord_url_webhook"]

    # Discord body alert.
    data = {
        "username" : "- PFSTALKER -",
        "embeds" : [
            {
                "color": 6311600,
                "title": alert_msg,
                "fields": [{
                    "name": "pfSense.",
                    "value": hostname,
                    "inline": "true"
                    }, {
                        "name": "IPv4.",
                        "value": ipv4,
                        "inline": "true"
                        }]
                }
            ]
        }

    # Perform webhook request.
    data = json.dumps(data)
    cmd = f"{curl} -X POST -H 'Content-Type: application/json' '{discord_webhook}' -d '{data}'"
    sb.getoutput(cmd)


# Telegram sender.
def send_telegram(alert_msg, local_info, config):
    """ Revice string 'alert_msg', object 'local_info' and send alert through curl to Telegram webhook. """

    # Set localhost information.
    hostname = local_info["name"]
    ipv4 = local_info["ipv4"]
    curl = local_info["curl"]

    # Set token and id to request webhook.
    telegram_bot_token = config["webhooks_config"]["telegram_bot_token"]
    telegram_chat_id = config["webhooks_config"]["telegram_chat_id"]

    # Telegram alert body.
    msg = f'''`- PFSTALKER -`
    ```sh\n{alert_msg}\n\npfSense: {hostname}\nIPv4: {ipv4}
    ```
    '''

    # Perform webhook request.
    cmd = f"{curl} -s -X POST https://api.telegram.org/bot{telegram_bot_token}/sendMessage -d chat_id={telegram_chat_id} -d text='{msg}' -d parse_mode=MarkdownV2"
    sb.getoutput(cmd)


# Call senders functions.
def report(alert_msg, config):
    """ Call all senders functions configured. """

    # Get localhost information to pass throug alert.
    local_info = localhost_info()

    # Discord reporting.
    send_discord(alert_msg, local_info, config)

    # Telegram reporting.
    send_telegram(alert_msg, local_info, config)


if __name__ == "__main__":
    # Start script execution.

    # Read config.
    with open("config.json", "r") as c:
        c = json.load(c)

    # Admin hash var.
    admin_hash = None

    # Start loop
    while True:

        # Verify admin hash.
        admin_hash = vrf_admin_hash(admin_hash)
        if admin_hash == None:
            report("Admin user password change!", c)

        # Verify SSH authorized key.
        if vrf_ssh_key(c) != True:
            report("SSH public key was deploy!", c)

        # Verify SSH authorized key.
        if vrf_ssh_service() == False:
            report("Service SSH was started!", c)

        # Loop sleep seconds.
        time.sleep(1)
