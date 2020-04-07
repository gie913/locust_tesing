#untuk python < 3, untuk python 3 pakainya configparser-nya huruf kecil
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('ConfigFile.properties')
print(config.get('DatabaseSection', 'database.dbname'))