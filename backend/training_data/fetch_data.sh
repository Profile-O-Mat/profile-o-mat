set -ue

mkdir partys
mkdir mdbs
python3 get_abgeordnete.py
python3 load_bios.py
python3 get_accounts_from_twde_list.py
python3 get_afd_kandidaten.py
python3 get_piraten_kandidaten.py
./golang_retrive_tweets 
amnt=$(ls -R -asl | grep .TXT | wc -l)
echo Read $amnt tweets!
