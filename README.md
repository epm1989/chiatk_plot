
# SWAR re-use 

- check and modified config.yaml and set the chia_location, for instance 
```bash
chia_location: /usr/lib/chia-blockchain/resources/app.asar.unpacked/daemon/chia
```  

    
modified swar chia plot manager only for check status

we only use view command
```bash
commands.py funtion view()
```

we updated an added a new function for getting processes and integrated tortoise
```bash
processes.py funtion get_running_plots()
processes.py funtion update_plot()
```

execute
```bash
python manager.py status
```
