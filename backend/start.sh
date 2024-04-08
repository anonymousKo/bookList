target_dir=$(cd $(dirname $0); pwd)
cd ${target_dir}
nohup python app.py > output.log 2>&1 &

