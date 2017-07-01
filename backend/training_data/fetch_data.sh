mkdir partys
mkdir mdbs
source twitter_keys.sh
python3 get_abgeordnete.py
python3 load_bios.py
python3 get_accounts_from_twde_list.py
python3 get_afd_kandidaten.py
./golang_retrive_tweets
