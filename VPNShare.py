import os
print ("\n\n\n\t\t\t      VPN Share:Script Made by Ankur Pandey")
print ("\t\t\t\thttps://github.com/ankurpandeyvns")
print ("\n\n\n")
print ("\t\t\t\tSharing Your VPN over Ethernet\n\n\n")
choice="X"
HOME=os.getenv("HOME")
os.popen("mkdir -p ~/VPNShare")
while(choice != "N" and choice != "Y"):
    choice=input("Do you want to be prompted to enter password everytime you share your VPN Connection? (Y/N)\t")
f=open(HOME+"/VPNShare/Share.sh","w+")
f.writelines(["#!/bin/bash\n",'cd "$(dirname ${BASH_SOURCE[0]})"\n'])
if(choice == "N"):
    print ("\n\n\t\t Remember!! Storing password in PLAINTEXT can be a huge security risk!! Proceed at your own risk..")
    psswd=input("\n\n\nEnter your password: ")
    f.write("echo "+psswd+" | sudo -S ./natvpn.sh")
else:
    f.write("sudo ./natvpn.sh")
f.close()
output = os.popen("ifconfig | grep 'utun\|inet.*-->' | sed -E 's/[[:space:]:].*//;/^$/d'").read().split()
for x in range(len(output)):
    tmp="ifconfig "+output[x]+" | awk '{print $1}'"
    if("inet" in os.popen(tmp).read().split()):
        iface=output[x]
        break
fscript="nat on "+iface+" from 192.168.137.1/24 to any -> ("+iface+")"
os.popen("echo '"+fscript+"' > ~/VPNShare/pfscript")
f=open(HOME+"/VPNShare/natvpn.sh","w+")
f.writelines(['#!/bin/bash\n','sudo sysctl -w net.inet.ip.forwarding=1\n','sudo pfctl -d\n','sudo pfctl -e -f pfscript'])
f.close()
os.popen("chmod +x ~/VPNShare/Share.sh | chmod +x ~/VPNShare/natvpn.sh | ln -s ~/VPNShare/Share.sh ~/Desktop/SHARE")
print ("Scripts are stored at : "+HOME+"/VPNShare")