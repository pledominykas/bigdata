#Configure our config servers replica set
docker exec -it mongocfg1 bash -c "echo 'rs.initiate({_id: \"mongocfg\",configsvr: true, members: [{ _id : 0, host : \"mongocfg1\" },{ _id : 1, host : \"mongocfg2\" },{ _id : 2, host : \"mongocfg3\" }]})' | mongosh"
docker exec -it mongocfg1 bash -c "echo 'rs.status()' | mongosh"

# Configure our shard servers replica set 1
docker exec -it mongors1n1 bash -c "echo 'rs.initiate({_id : \"mongors1\", members: [{ _id : 0, host : \"mongors1n1\" },{ _id : 1, host : \"mongors1n2\" },{ _id : 2, host : \"mongors1n3\" }]})' | mongosh"
docker exec -it mongors1n1 bash -c "echo 'rs.status()' | mongosh"

# Configure our shard servers replica set 2
docker exec -it mongors2n1 bash -c "echo 'rs.initiate({_id : \"mongors2\", members: [{ _id : 0, host : \"mongors2n1\" },{ _id : 1, host : \"mongors2n2\" },{ _id : 2, host : \"mongors2n3\" }]})' | mongosh"
docker exec -it mongors2n1 bash -c "echo 'rs.status()' | mongosh"

# Add the shard to the cluster
docker exec -it mongos1 bash -c "echo 'sh.addShard(\"mongors1/mongors1n1\")' | mongosh"
docker exec -it mongos1 bash -c "echo 'sh.addShard(\"mongors2/mongors2n1\")' | mongosh"
docker exec -it mongos1 bash -c "echo 'sh.status()' | mongosh"

# Enable sharding on a database
docker exec -it mongors1n1 bash -c "echo 'use big_data_db' | mongosh"
docker exec -it mongos1 bash -c "echo 'sh.enableSharding(\"big_data_db\")' | mongosh"

# Enable sharding on a collection, sharding key:
docker exec -it mongors1n1 bash -c "echo 'db.createCollection(\"big_data_db.vessels\")' | mongosh"
docker exec -it mongors1n1 bash -c "echo 'db.createCollection(\"big_data_db.filtered_vessels\")' | mongosh"
docker exec -it mongos1 bash -c "echo 'sh.shardCollection(\"big_data_db.vessels\", {\"mmsi\" : \"hashed\"})' | mongosh"
docker exec -it mongos1 bash -c "echo 'sh.shardCollection(\"big_data_db.filtered_vessels\", {\"mmsi\" : \"hashed\"})' | mongosh"
