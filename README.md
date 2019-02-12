# pyspark project template

## 前置作業

若為 MacOS 需安裝與 linux 一致的 getopt

```bash
brew install gnu-getopt
echo 'export PATH="/usr/local/opt/gnu-getopt/bin:$PATH"' >> ~/.bash_profile
```

## 一鍵安裝

```sh
$ ./build_tool/build.sh -h
[Installation]
    Usage: build.sh [OPTIONS] ENV (dev|ut|uat|prod)
     e.g. build.sh -b dev
    OPTIONS:
       -h|--help                             Show this message
       -b|--build                            Build project
       -c|--clean                            Clean last build result
       -r|--rebuild                          Rebuild Project
       -p|--python                           Python version (Default:2) e.g. --python 2.7
```

- 執行 build

```
build_tool/build.sh -b dev -p 2.7
```

## 手動安裝

- create venv

```
virtualenv venv
```

- enter into virtual env

```
source venv/bin/activate
```

- install all libs in py_pkg in virtual env

```
python setup.py lib -p py_pkg [--pip-args="-i <index-url> --trusted-host=<host>"]
```

- install pkg in your module

```
python setup.py install [--pip-args="-i <index-url> --trusted-host=<host>"]
```

- [opt] install dev-libs from extras_require
```
python setup.py extra [-k <key>] [--pip-args="-i <index-url> --trusted-host=<host>"]
```

- leave venv

```
deactivate
```

## 啟動主程式

- execute

```
bin/start-job.sh
```

## 設定檔

### 確認各環境的設定檔 conf/\*.conf

- conf/env.conf

設定 `bin/start-job.sh` 執行時所需參數，e.g. `spark` 相關的資源參數

- runtime-env-info.sh

設定環境路徑

- job.conf

程式執行時的參數設定檔，可自行擴充，檔案  格式為 [hoconf](https://github.com/chimpler/pyhocon)

e.g.

```json
job.name=project-template
databases.active = true
databases.enable_logging = false
databases.home_dir = /Users/darthbear
```

---

- test your project

```
# pytest
python setup.py test

# pytest - with specific pypi server
python setup.py test --pip-args="-i <index-url> --trusted-host=<host>"

# pytest - disable requirements check
python setup.py test --disable-check

# pytest - with argument
python setup.py test --pytest-args="-vvv"

# pytest - with multiple arguments
python setup.py test --pytest-args="-q -vvv"

# pytest - only test your module (without modules in py_pkg)
python setup.py test --pytest-args="tests"
```

- clean build files

```
# clean without .egg folder
python setup.py clean

# clean with .egg folder
python setup.py clean -e
```

### requirements

`docs`資料夾下有三個`requirements檔案`
* requirements: 第三方套件

範例：
```
click==6.6
```
* requirements-lib: local 套件
> 套件程式需放在`py_pkg`資料夾內，且符合setuptool格式．建構專案時會安裝在`py_pkg`資料夾內的所有程式

測試方式：
```
cd py_pkg/cathay-spark
python setup.py bdist_wheel
```
正確的話會在 py_pkg/cathay-spark/dist 看到.whl檔案

範例：
```
py_pkg/cathay-spark/dist/cathay_spark-1.0-py2-none-any.whl
cathay-spark==1.0
```
* requirements-dev: 測試套件
範例：
```
pytest==3.7.4
```
