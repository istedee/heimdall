### Environment setup

Run these commands from the src directory.

### Installation

**For Linux/MacOS**

Install dependencies:

```shell
$ sudo apt install libcurl4-gnutls-dev librtmp-dev
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

Use the following command from Heimdall folder.

```shell
$ python3 -m heimdall.main
```

To run from e.g src folder level, use command prefix:

```shell
$ python3 -m Heimdall.heimdall.main
```

This will set the package path correctly
