# start hadoop and yarn
service sshd start
hdfs namenode -format
/bin/bash $HADOOP_HOME/sbin/start-dfs.sh
/bin/bash $HADOOP_HOME/sbin/start-yarn.sh

# start hive metastore
service mysqld start
mysqladmin --user=root password "admin"
hive --service metastore

# upload data to HDFS
hadoop fs -mkdir /data/
hadoop fs -put /usr/data/* /data/

# create hive table renting_house
hive -f /usr/create_table.hql
