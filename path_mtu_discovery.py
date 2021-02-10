import os
from subprocess import call
import csv
from datetime import datetime


def path_mtu_finder(mrbts_ip):
    success=0
    fail=65500
    is_65500_flag=0
    s=fail

    while fail-success!=1:
        ping_reply=call(['ping','-c','1','-s',str(s),mrbts_ip])
        if ping_reply==0:
            success=s
            if is_65500_flag==0:
                break
        else:
            fail=s
        s=int(success+((fail-success)/2))
    
    return success


def csv_writer(all_sites_path_mtu):
    with open(os.path.join(os.getcwd(),'path_mtu_output.csv'),'w',newline='') as f_out:
        csv_header=['MRBTS ID','MRBTS IP','PATH MTU']
        csv_writer=csv.DictWriter(f_out,fieldnames=csv_header)
        csv_writer.writeheader()

        for site in all_sites_path_mtu:
            csv_writer.writerow(site)
    print("OUTPUT CSV file created with Path MTU information for {} sites.".format(len(all_sites_path_mtu)))

        
def main():
    print("Starting PATH MTU Discovery script ...")
    start_time=datetime.now()

    all_sites_path_mtu=[]
    with open(os.path.join(os.getcwd(),'mPlane_IP.csv'),'r',newline='') as f_in:
        csv_reader=csv.DictReader(f_in)
        for row in csv_reader:
            mrbts_id=row['MRBTS ID']
            mrbts_ip=row['mPlane IP']

            ping_response_size_zero=call(['ping','-c','1','-s','0',mrbts_ip])
            if ping_response_size_zero!=0:
                all_sites_path_mtu.append({'MRBTS ID':mrbts_id,'MRBTS IP':mrbts_ip,'PATH MTU':'O&M Down'})
                continue
            
            path_mtu=path_mtu_finder(mrbts_ip)
            all_sites_path_mtu.append({'MRBTS ID':mrbts_id,'MRBTS IP':mrbts_ip,'PATH MTU':path_mtu})
        
    csv_writer(all_sites_path_mtu)
    
    print("Script complete. Total time taken : {} seconds.".format((datetime.now()-start_time).seconds))





main()





