### EPS Project Summary


### Tasks

1) Consolidate relevant 

### Privacy Measures:
- for each strategy, a reference to a paper would be nice for credibility 

**Noise Measures**
1) Noise in broadcast GPS coordinates - Ian
- [commit](https://github.com/icmccorm/v2x-privacy-sim/commit/b37b70962cc7ae447cea82d39e6bbaa534954502)
2) speed
3) acceleration
4) heading (look into this)


**BSM Characteristic**
- Hz - messages per second

**credential rotation** --> require re running simulation
1) number of credentials allocated 
2) credential change rule (distance traveled, messages sent, random, baseline (every 10 seconds))


**adversary**
1) number of observation zones
2) distribution of observation zones


### Privacy Metrics:
- recall: 
- precision:
- in a given observation zone, set of unique credentials, likelihood estimate with every other credential (entropy)
    - instead of just looking at the accuracy of classification (precision, recall, f1), you could look at the "matching" likelihood for each observed credential
    - knowing this will explain "why" some schemes are worse than others



### Privacy budget
- how usable is the system given a privacy measure scheme
- https://www.usenix.org/system/files/sec19-jayaraman.pdf


### Visualizations
- precision/recall for different parameters?
- adversary uncertainty about linkage for credential i
- ...


### tasks
1) miguel - VEIN simulator; try to run
2) ray - making TDrive data work with code
3) luke - how credential linkage likelihood measure works 
4) ian - 


tasks we can implement on the data from the paper; 
2) 

1) Noise in broadcast speed - Ian
- [commit](https://github.com/icmccorm/v2x-privacy-sim/commit/41413edd8a6589fee532a48c35622b5ec440887a)
