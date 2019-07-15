# bixpe

### To have the schedule to the minute with bixpe:

in manifest [bixpe.yml](https://github.com/alvarezbruned/bixpe/blob/master/bixpe.yml) the default action it's "start", the available actions are commented.

To run script just execute:

```
docker-compose -f bixpe.yml up -d
```

to stop the deploy just need execute:

```
docker-compose -f bixpe.yml down -v
```



## Or by docker
Need execute first:
xhost +local:docker
to share your X
executing docker-compose up -d (needs set credentials before)

