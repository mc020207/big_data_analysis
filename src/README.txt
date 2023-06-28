文件组成

demodata/ 经处理的数据输出
demorawdata/ 待处理的原始demo数据
demo_frontend.py 为前端展示代码
fpgrowth.py 为提交给spark运行的代码
load_to_database.py 为将运算结果保存到数据库的代码
preprocess.py 为对输入数据进行预处理的代码
data_support_4e-6_confidence_0.4.zip 完整数据跑出来的输出，可以作为参考示例

demo流程
1、使用preprocess.py处理demorawdata数据,保存到demodata

2、将输出移动到nfs目录中，经过挂载nfs，使得spark的executer、worker在目录/mydata/data文件可以访问到数据

3、通过spark-submit命令等方法运行fpgrowth.py。
这一部分的命令可能比较复杂，仅给出示例。
在master pod执行
/opt/spark/bin/spark-submit \
      --master k8s://https://10.176.62.221:6443 \
      --deploy-mode cluster \
      --conf spark.executor.instances=5 \
      --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
      --conf spark.kubernetes.namespace=spark-cluster \
      --conf spark.kubernetes.driver.pod.name=spark-wctest-1 \
      --conf spark.kubernetes.container.image=awayee/spark-py:add_numpy\
      --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.data.mount.path=/mydata \
      --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.data.mount.readOnly=false \
      --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.data.options.claimName=mypvc2 \
      --conf spark.kubernetes.executor.volumes.persistentVolumeClaim.data.mount.path=/mydata \
      --conf spark.kubernetes.executor.volumes.persistentVolumeClaim.data.mount.readOnly=false \
      --conf spark.kubernetes.executor.volumes.persistentVolumeClaim.data.options.claimName=mypvc2 \
      --conf spark.executor.heartbeatInterval=100s\
      --name spark_fpgrowth_1 \
      local:///mydata/fpgrowth.py

我们需要起一些driver pod、worker pod，需要将nfs目录在K8S中设置为PV，并设置相关PVC；
我们还对spark镜像做了一些处理，安装上了numpy  

4、将对应挂载位置的/mydata/output的csv文件（请不要放其他文件）取出放到sparkoutput

5、配置数据库

6、使用load_to_database.py将数据存入数据库（load_to_database.py采用了硬编码，所以需要根据情况改一下）

7、运行demo_frontend.py

