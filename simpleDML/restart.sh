for pid in `ps -ewf|grep admin.py | grep -v "grep" | awk '{print $2}'`
do
  kill -9 $pid
done

python admin.py 
