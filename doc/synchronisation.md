# Clock synchronisation between robots
## Synchronisation
  The clock synchronisation uses [chrony]( https://chrony.tuxfamily.org/chrony )
  which is a versatile implementation of the Network Time Protocol (NTP).

  Chrony should be installed in all the robots (slaves) and the server used as a reference (master) :
  
    sudo apt-get install chrony
  
  The configuration of chrony is done in the file `/etc/chrony/chrony.conf`.
  The configuration for slaves is available in [../tools/chrony.conf](../tools/chrony.conf).
  For a local network `192.168.team_id.0/8`, master configuration is
  
     local stratum 8
     manual
     allow 192.168.9.0/8
     rtcsync
     
 the slaves configuration is
 
     server master_ip maxdelay 0.005 minpoll 0 maxpoll 0
     allow 192.168.9.0/8
     rtcsync
     
## Updating a slave configuration

Stop current chronyd

    sudo killall chronyd

Restart chronyd

    sudo chronyd
     
## Monitoring
  From a slave, we can check the offset to master using 
  
    chronyc -n sources
    
  To monitor the offset between master and robots, the script
  [../tools/chrony_monitoring.py](../tools/chrony_monitoring.py) can be used.
  The script shows the measured offset between the clocks in milliseconds.
  For example
  
    ./chrony_monitoring.py olive tom > /tmp/offsets.csv
    
  and in an other terminal launch gnuplot and type
  
    plot for [col=2:k] '/tmp/offsets.csv' using 0:col
    
  where `k` is 1 plus the number of robots, so `k=3` for our example.
 

 
  

  
  

