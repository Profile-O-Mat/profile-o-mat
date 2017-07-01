package main

import (
	"fmt"
	"os"
	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
	"io/ioutil"
	"sync"
)

func tweetLookup(c *twitter.Client, wg *sync.WaitGroup, u string, p string) {
	user, _, _ := c.Timelines.UserTimeline(&twitter.UserTimelineParams{
		ScreenName:      u,
		ExcludeReplies:  twitter.Bool(true),
		IncludeRetweets: twitter.Bool(false),
		Count:           200,
	})
	for t := range user {

		ioutil.WriteFile("partys/"+p+"/"+u+"/"+user[t].IDStr+".TXT", []byte(user[t].Text), 0755)
	}
	fmt.Println(u)
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
			wg.Add(1)
			go tweetLookup(client, &wg, mdb.Name(), party.Name())
		}
	}
	// User Show
	wg.Wait()
}
