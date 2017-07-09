package main

import (
	"fmt"
	"os"
	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
	"io/ioutil"
	"sync"
)

func tweetLookup(c *twitter.Client, wg *sync.WaitGroup, u string, p string, sId int64) {
	wg.Add(1)

	var timeLineVar twitter.UserTimelineParams
	if sId == 0	{
		timeLineVar = twitter.UserTimelineParams{
			ScreenName:      u,
			ExcludeReplies:  twitter.Bool(true),
			IncludeRetweets: twitter.Bool(false),
			Count:           200,
		}
	} else {
		timeLineVar = twitter.UserTimelineParams{
			ScreenName:      u,
			ExcludeReplies:  twitter.Bool(true),
			IncludeRetweets: twitter.Bool(false),
			Count:           200,
			SinceID:		 sId,
		}
	}
	user, _, _ := c.Timelines.UserTimeline(&timeLineVar)
	for t := range user {
		ioutil.WriteFile("partys/"+p+"/"+u+"/"+user[t].IDStr+".TXT", []byte(user[t].Text), 0755)
	}
	if len(user) > 0 {
		fmt.Println(u + "\t\t=>", len(user), "\t\t->", user[len(user)-1].ID)
		go tweetLookup(c, wg, u, p, user[len(user)-1].ID)
	} else {
		fmt.Println(u + "\t\t=>", len(user), "\t\t->")
	}
	wg.Done()
}

func main() {
	fmt.Println("Hello")

	config := oauth1.NewConfig(os.Getenv("CONSUMER_KEY"), os.Getenv("CONSUMER_SECRET"))
	token := oauth1.NewToken(os.Getenv("ACCESS_TOKEN_KEY"), os.Getenv("ACCESS_TOKEN_SECRET"))
	httpClient := config.Client(oauth1.NoContext, token)
	wg := sync.WaitGroup{}
	// Twitter client
	client := twitter.NewClient(httpClient)
	partys, _ := ioutil.ReadDir("partys")
	for _, party := range partys {
		mdbs, _ := ioutil.ReadDir("partys/" + party.Name())
		for _, mdb := range mdbs {
			fmt.Println(party.Name(), mdb.Name())
			go tweetLookup(client, &wg, mdb.Name(), party.Name(), 0)
		}
	}
	// User Show
	wg.Wait()
}
