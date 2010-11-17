#!/usr/bin/env python

###
### Author : Hiemanshu Sharma <mail@theindiangeek.in>
###
###
### tweeter.py
###
### Python script to update twitter status
###
### TODO: Allow getting searches, add
### follow, unfollow, delete, list people you follow
###
###

import twitter, sys, ConfigParser, os.path

__author_ = "mail@theindiangeek.in"
version = 0.1

USAGE = '''Usage: tweeter.py command
    update <status>                      : Update your twitter status
    timeline [username]                  : Get your timeline or of username if username is specified
    replies                              : Get replies
    friends                              : Get list of friends
    follows                              : Get list of people that follow you
    direct                               : Get Direct messages sent to you
    senddirect <username> <text>         : Send Direct message to [username]
    search <text>                        : Search for [text] on twitter
    follow <username>                    : Follow [username]
    unfollow <username>                  : Stop following [username]
    createlist <name> [public/private]   : Create a list by the name given with public/private access (It is public by default)
 '''

DOCUMENTATION = '''The Consumer Key and Secret Pair and Access Token Key and secret pair are stored in ~/.tweetrc
The format for the file is : 
    [Tweet]
    conskey: <Consumer Key>
    conssec: <Consumer Secret>
    accstkn: <Access Token Key>
    accssec: <Access Token Secret>

To add the above keys use add-auth parameter in the format i.e.,
add-auth <Consumer Key> <Consumer Secret> <Access Token Key> <Access Token Secret>
You can get the above values by registering your app at http://dev.twitter.com
'''

### Check if config file has the section Tweet, if not add it
config = ConfigParser.ConfigParser()
if not config.has_section("Tweet"):
    config.add_section("Tweet")
    
### Print Usage if no arguments have been supplied

if len(sys.argv) == 1:
    print USAGE
    sys.exit(2)

if cmp(sys.argv[1],"-h") == 0:
    print USAGE 
    sys.exit(2)

### Check if file exists, if it doesn't exist and if user wants to add the keys
### If user doesn't want to add keys, show Documentation

check = os.path.isfile(os.path.expanduser('~/.tweetrc'))
if cmp(check,False) == 0:
    if cmp(sys.argv[1],"add-auth" == 0) and len(sys.argv) != 6:
        print sys.argv[1]
        print DOCUMENTATION
        sys.exit(2)
    elif cmp(sys.argv[1],"add-auth" == 0) and len(sys.argv) == 6:
        config.set("Tweet","conskey",sys.argv[2])
        config.set("Tweet","conssec",sys.argv[3])
        config.set("Tweet","accstkn",sys.argv[4])
        config.set("Tweet","accssec",sys.argv[5])
        config.write(open(os.path.expanduser('~/.tweetrc'),'w'))
        print "Access keys saved!"

### Read Keys from file

config.read(os.path.expanduser('~/.tweetrc'))
conskey = config.get("Tweet", "conskey", raw=True)
conssec = config.get("Tweet", "conssec", raw=True)
accstkn = config.get("Tweet", "accstkn", raw=True)
accssec = config.get("Tweet", "accssec", raw=True)

### Create api object to be used

api = twitter.Api(consumer_key=conskey, consumer_secret=conssec, access_token_key=accstkn, access_token_secret=accssec)
    
### Different checks to see what the user wants to do

if cmp(sys.argv[1],"update") == 0:
    if len(sys.argv) < 3:
        print USAGE
        sys.exit(2)
    status = ' '.join(sys.argv[2:])
    api.PostUpdates(status)
    print "Your status has been updated!"

if cmp(sys.argv[1],"timeline") == 0:
    statues = api.GetUserTimeline(sys.argv[2])
    for s in statues:
        print s.text

if cmp(sys.argv[1],"replies") == 0:
    replies = api.GetReplies()
    for l in replies:
        print "From : " + l.user.screen_name +  " \nMessage : %s\n" %l.text 

if cmp(sys.argv[1],"direct") == 0:
    directs = api.GetDirectMessages()
    for h in directs:
        print ("From : " + h.sender_screen_name + "\nMessage : %s\n" %h.text)

if cmp(sys.argv[1],"friends") == 0:
    friends = api.GetFriends()
    for k in friends:
        if cmp(k.name,k.screen_name) == 0:
            print ("Screen Name : %s" %k.screen_name)
        else:
            print ("Real Name :" + k.name +"        Screen Name: %s" %k.screen_name)

if cmp(sys.argv[1],"follows") == 0:
    follows = api.GetFollowers()
    for k in follows:
        if cmp(k.name,k.screen_name) == 0:
            print ("Screen Name : %s" %k.screen_name)
        else:
            print ("Real Name :" + k.name +"        Screen Name: %s" %k.screen_name)

if cmp(sys.argv[1],"senddirect") == 0:
    if len(sys.argv) < 4:
        print USAGE
        sys.exit(2)
    message = ' '.join(sys.argv[2:])
    dm = api.PostDirectMessage(sys.argv[2],message)
    print "Message sent to %s" %sys.argv[2]

if cmp(sys.argv[1],"search") == 0:
    if len(sys.argv) < 3:
        print USAGE
        sys.exit(2)
    search=api.GetSearch(' '.join(sys.argv[2]))
    for s in search:
        print "%s : %s" %(s.user.screen_name,s.text)

if cmp(sys.argv[1],"follow") == 0:
    if len(sys.argv) < 3:
        print USAGE
        sys.exit(2)
    k = api.CreateFriendship(sys.argv[3])
    print "You are now following " + k.user.screen_name

if cmp(sys.argv[1],"unfollow") == 0:
    if len(sys.argv) < 3:
        print USAGE
        sys.exit(2)
    u = api.DestroyFriendship(sys.argv[3])
    print "You are not following %s anymore" % k.user.screen_name

if cmp(sys.argv[1],"createlist") == 0:
    if len(sys.argv) < 3:
        print USAGE
        sys.exit(2)
    if len(sys.argv) == 4:
        l = api.CreateList('user',sys.argv[2],mode=sys.argv[3])
    if len(sys.argv) == 3:
        l = api.CreateList('user',sys.argv[2])
    print "List by the name %s has been created" %sys.argv[2]
