### Environment setup

Run these commands from the src directory.

### Installation

**For Linux/MacOS**

Install dependencies:

DO THIS BEFORE ANYTHING:

```
You need to install Docker and Docker compose. Depending on your system, install docker engine if you can. If you cant install engine.
```

This link for Docker: https://docs.docker.com/engine/install/

```
After installing you should check this link for group creations if you want
to run rootless.
```

Post-installation instructions: https://docs.docker.com/engine/install/linux-postinstall/

```
You should also install Docker compose. If you installed Docker Desktop you should have compose too.
```

Install Docker compose-plugin https://docs.docker.com/compose/install/

```shell
$ sudo apt install libcurl4-gnutls-dev librtmp-dev
$ sudo apt install nmap
```

Create virtual env:

```shell
$ python3 -m venv env
```

```shell
$ source env/bin/activate
```

```shell
$ pip install -r requirements.txt
```

**For Windows**

Create virtual env:

```shell
$ python -m venv env
```

```shell
C:\> env\Scripts\activate.bat
```

```shell
pip install -r requirements.txt
```

---

### Installation

#### ELK

First you should initialize elk-component. cd yourself to the elk-folder.

```shell
$ cd src/elk/
```

Run startup-script in the folder. Give priviledges if needed

Give priviledges

```shell
$ chmod +x startup.sh
```

Run script

```shell
$ ./startup.sh
```

This script may take more time if you don't have elastic- and kibana-images from Docker. After pulling the images startup time will reduce.

If you want to stop elk-component you can then run shutdown command for compose. You need to be in the elk-directory.

```shell
$ (sudo) docker compose down
```

When you have started elk you can then start the Heimdall service.

#### Heimdall

Start Heimdall with the 'start_heimdall.sh' script

```shell
chmod +x start_heimdall.sh
./start_heimdall.sh
```
