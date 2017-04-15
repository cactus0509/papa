for pid in `netstat -ntpl | grep 8080 | awk '{print $7}' | awk -F"/" '{print $1}'`
do
  kill -9 $pid
done

sleep 5 
nohup python admin.py 10001 &
nohup python admin.py 10002 &
nohup python admin.py 10003 &
nohup python admin.py 10004 &
nohup python admin.py 10005 &
