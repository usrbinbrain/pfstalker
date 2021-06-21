<p align="center">
  <img alt="Discord" src="https://i.imgur.com/smRIjAi.png" title="PFSTALKER" width="35%">
</p>

# PFSTALKER

### _Supervises pfSense SSH service status and admin credentials, deploy SSH public key and sends alerts through Telegram and Discord webhooks._

![GitHub](https://img.shields.io/github/license/usrbinbrain/pfstalker?color=darkgreen)

Verify SSH service status performing restart of service if not runnig, detect changes on admin user credentials (password hash modification), perform deployment, verification and rollback of your SSH public key in admin user's authorized_keys file, send all alerts through Telegram and Discord webhooks.

Running as a FreeBSD daemon on pfSense.
***

### Features. :jigsaw:

- [x] Run as a FreeBSD daemon.
- [x] Detect admin password changes.
- [x] Deploy and verify SSH public key.
- [x] Monitor and restart SSH service.
- [x] Send alerts through Discord webhook and Telegram bot.

***

### Download. :octocat:

Access your pfSense and clone this repo with bellow git or curl commands.

```bash
# Clone repo using git.
git clone https://github.com/usrbinbrain/pfstalker.git

# Clone repo using curl.
curl -L -O https://github.com/usrbinbrain/pfstalker/archive/refs/heads/master.zip && unzip -d ./pfstalker/ -j master.zip
```
***

### Install. :gear:

The `install.sh` script will create a service configuration file to run `pfstalker.py` as a FreeBSD [daemon](https://www.freebsd.org/cgi/man.cgi?query=daemon&sektion=8).

Access repo directory and exec this install script to create pfstalker service, run bellow command on your pfSense.

```bash
# Access dir and exec install.sh script.
cd pfstalker/ && /bin/sh install.sh
```

***

### Configure. :wrench:

Set your SSH public key, webhook Discord, Telegram bot token and chat id in the `config.json` file.

The SSH public key configured in this file will be implemented and verified in the admin authorized_keys file.

You can choose to receive alerts via Discord or Telegram, but pfstalker can send alerts using both platforms together.

- _Discord webhook_.

For recive alerts through Discord channel, configure your Discord [webhook](https://support.discord.com/hc/en-us/articles/228383668-Usando-Webhooks) url on [discord_url_webhook](https://github.com/usrbinbrain/pfstalker/blob/main/config.json#L3) key value.

```bash
"discord_url_webhook": "https://discord.com/api/webhooks/0000/YOUR_DISCORD_WEBHOOK_FULL_URL"
```

- _Telegram bot_.

For recive alerts through Telegram, create your bot using [Botfather](https://core.telegram.org/bots#6-botfather) and add your bot [token](https://core.telegram.org/bots/api#authorizing-your-bot) on [telegram_bot_token](https://github.com/usrbinbrain/pfstalker/blob/main/config.json#L4) key value and your bot [chat id](https://core.telegram.org/bots/api#chat) on [telegram_chat_id](https://github.com/usrbinbrain/pfstalker/blob/main/config.json#L5) value key.

```bash
"telegram_bot_token": "00000000:YOUR_TELEGRAM_BOT_TOKEN",
"telegram_chat_id": "0000_YOUR_BOT_CHAT_ID_0000"
```

- _SSH key_.

Set your SSH public key inside [ssh_public_key](https://github.com/usrbinbrain/pfstalker/blob/main/config.json#L7) list to pfstalker perform deploy and rollback on authorized_keys file.

```bash
origkey = 'ssh-rsa AAAAB3N__YOUR_SSH_PUBLIC_KEY___Y07JYLSD yourname@yourhostname'
```
***

### Restart pfstalker. :joystick:

After configured `config.json` file, just restart pfstalker service created by `install.sh` script on install step.

Now you can manage pfstalker service as a FreeBSD daemon service, performing `start`, `stop`, `restart` and `status` about this daemon.

To start supervisor of pfstalker on your pfSense firewall, just restart the service with bellow command.

```bash
# Restarting service on pfSense firewall.
/usr/local/etc/rc.d/pfstalker restart
```
***

### Alerts. :bulb:

There are currently 3 different alerts sent by pfstalker to Discord and Telegram.

You can see this alerts on bellow pictures.

> - Admin user password change!

> This alert is send if pfstalker identify any change on admin user hash on /etc/master.passwd.

<p align="center">
  <img alt="Discord" src="https://i.imgur.com/9Qu0fiZ.png" title="Admin password alert on Discord web." width="40%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="Telegram" src="https://i.imgur.com/evhHkeS.png" title="Admin password alert on Telegram web." width="40%">
</p>

> - SSH public key was deploy!

> This alert is send if pfstalker perform deploy or rollback of SSH public key on authorized_keys file.

<p align="center">
  <img alt="Discord" src="https://i.imgur.com/wVL3m2p.png" title="SSH key alert on Discord web." width="40%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="Telegram" src="https://i.imgur.com/YwEjqu4.png" title="SSH key alert on Telegram web." width="40%">
</p>

> - Service SSH was started!

> If pfstalker restart SSH service on pfSense firewall, this alert is send.

<p align="center">
  <img alt="Discord" src="https://i.imgur.com/9BRCirG.png" title="SSH service alert on Discord web." width="40%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="Telegram" src="https://i.imgur.com/4qN8yaF.png" title="SSH service alert on Telegram web." width="40%">
</p>

***
