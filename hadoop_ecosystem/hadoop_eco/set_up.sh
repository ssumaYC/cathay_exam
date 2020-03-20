# install required tool for hadoop
yum -y install openssh*
yum -y install rsync
yum -y install tar
yum -y install which

# untar the tars to /opt
for file in $(ls -d /usr/downloads/tars/*)
do
	tar -zxvf $file -C /opt
done

#export env needed
cat env >> ~/.bashrc
rm env
source ~/.bashrc

# hadoop settings
echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
rsync -a /usr/hadoop_conf/ $HADOOP_HOME/etc/hadoop/
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

# hive settings
cp /usr/downloads/jars/* $HIVE_HOME/lib/
rsync -a /usr/hive_conf/ $HIVE_HOME/conf/
yum -y install mysql-server

# spark settings
cp /usr/downloads/jars/* $SPARK_HOME/jars/
rsync -a /usr/hive_conf/ $SPARK_HOME/conf/

# install python3.6
yum -y install gcc openssl-devel bzip2-devel sqlite-devel
cd /opt/Python-3.6.5
./configure --enable-optimizations
make altinstall
python3.6 -m pip install elasticsearch
python3.6 -m pip install jieba

rm -rf /usr/downloads/
