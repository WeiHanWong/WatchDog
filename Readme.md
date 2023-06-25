# WatchDog

## Prereq.

**macOS/Linux**

```bash
sudo apt install libpq-dev
sudo apt install postgresql
sudo apt install bluetooth libbluetooth-dev
sudp apt install opencv-python
sudo -i -u postgres
psql
\password

```

## Set up & Installation.

### 1 .Clone/Fork the git repo and create an environment 
                    
**Windows**
          
```bash
git clone https://github.com/WeiHanWong/WatchDog.git
cd WatchDog
py -3 -m venv venv

```
          
**macOS/Linux**
          
```bash
git clone https://github.com/WeiHanWong/WatchDog.git
cd WatchDog
python3 -m venv venv

```

### 2 .Activate the environment
          
**Windows** 

```venv\Scripts\activate```
          
**macOS/Linux**

```. venv/bin/activate```
or
```source venv/bin/activate```

### 3 .Install the requirements

Applies for windows/macOS/Linux

```
pip install -r requirements.txt
pip install psycopg2
```

### 4. Run the application 

```
flask run
```
