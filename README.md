# MongoDB 4.0 Sharding with Remote Access

To simplify, this test is built on a structure using one mongos, one config server and two shards. Hence, 4 real or virtual machines in total.

## 1. Config Ip Address
Check the ip addresses and host name of each machine and copy paste to all 4 machines. 
In each virtual machine:
```
cd /etc
sudo nano hosts
```
Paste ip addresses
```
10.10.10.xx	router
10.10.40.xx	config
10.10.40.xx	shard1
10.10.40.xx	shard2
```
## 2. Install Same Version of MongoDB in all four machines
Use MongoDB 4.0 in this program.
You can copy the following command line by line into shell with sudo or create an installmongo.sh file and copy all lines into it, excute by 'sudo bash installmongo.sh'.
```
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
apt-get update
apt-get install -y mongodb-org
```

## 3. Launch Mongod on Each Shard Machine
Create the data folder (it can be anywhere) and kill any existing mongod process:
```
sudo mkdir -p /data/db
sudo chmod -R 777 /data/db
sudo killall -q mongod
```
Create configuration file shard.conf and copy following code into it:
```
storage:
    dbPath: "/data/db"
 
replication:
    replSetName: "rs1"
net:
    bindIp: 0.0.0.0
    port: 27018
sharding:
    clusterRole: "shardsvr"
```
Launch mongod for the shard:
```
mongod --config shard.conf
```
Keep this service running and open another terminal.
Create a mongo instance through
```
mongo localhost:27018 
# or mongo --host localhost --port 27018 
```
Initiate the replica set in mongo shell:
```
rs.initiate()
```
In shard2, do same steps but remember to change *replSetName* in shard.conf from rs1 to rs2
## 4. Launch Mongod on the Config Machine
Create the config folder (it can be anywhere) and kill any existing mongod process:
```
sudo mkdir -p /data/configdb 
sudo chmod -R 777 /data/configdb 
sudo killall -q mongod
```
Create configuration file svrconfig.conf and cpoy following code into it:
```
storage:
    dbPath: "/data/configdb"
    journal:
        enabled: true
net:
    bindIp: 0.0.0.0
    port: 27019

sharding:
    clusterRole: configsvr
replication:
    replSetName: cfg1
```
Launch mongod for config server:
```
mongod --config svrconfig.conf
```
Keep this service running, in another shell: create mongo instance and Initiate the replica set:
```
mongo localhost:27019 
mongo> rs.initiate()
```
## 5. Launch mongos on the Router Machine
Create config file mongos.conf
```
sharding:
    configDB: cfg1/config
net:
    port: 27017
    bindIp: 0.0.0.0
```
Launch mongos service
```
mongos --config mongos.conf
```
Keep this terminal running.
## 6. Configure the Cluster on Router Machine
In another terminal, on the mongos(router) machine, connect to the mongos process and add shards:
```
mongo localhost:27017
sh.addShard("rs1/shard1:27018")
sh.addShard("rs2/shard2:27018")
```
Enable sharding for your database and collections
```
sh.enableSharding("robots")

sh.shardCollection("robots.task", {_id:1})
# note: this needs to be done again after a collection drop.
```
Configration finished. Check the status of the cluster:
```
mongos> sh.status()
--- Sharding Status --- 
  sharding version: {
  	"_id" : 1,
  	"minCompatibleVersion" : 5,
  	"currentVersion" : 6,
  	"clusterId" : ObjectId("5cb4a3c22a4dd1926e8709e9")
  }
  shards:
        {  "_id" : "rs1",  "host" : "rs1/ubuntu3:27018",  "state" : 1 }
        {  "_id" : "rs2",  "host" : "rs2/ubuntu4:27018",  "state" : 1 }
  active mongoses:
        "4.0.9" : 1
  autosplit:
        Currently enabled: yes
  balancer:
        Currently enabled:  yes
        Currently running:  no
NaN
        Failed balancer rounds in last 5 attempts:  0
        Migration Results for the last 24 hours: 
                No recent migrations
  databases:
        {  "_id" : "tests",  "primary" : "rs2",  "partitioned" : true }
                tests.vquest_metadata
                        shard key: { "_id" : 1 }
                        unique: false
                        balancing: true
                        chunks:
                                rs2	1
                        { "_id" : { "$minKey" : 1 } } -->> { "_id" : { "$maxKey" : 1 } } on : rs2 Timestamp(1, 0) 
mongos>
```
## 7. Allow Remote Access
If you want to allow user 'rosie' to get access to database 'tests' to achieve read and write:
```
use tests

db.createUser({
    user: 'rosie',
    pwd: 'mypwd',
    roles: [{ role: 'readWrite', db:'robots'}]
})
```
Then, in your python code, get remote access through:
```
# use your mongos(router) machine ip and port here
client = MongoClient("mongodb://rosie:mypwd@10.10.10.xx:27017/robots")
```
