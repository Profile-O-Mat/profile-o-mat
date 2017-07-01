package main

import (
	"fmt"
	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
	"io/ioutil"
	"sync"
)

func tweetLookup(c *twitter.Client, wg *sync.WaitGroup, u string, p string) {
	user, _, _ := c.Timelines.UserTimeline(&twitter.UserTimelineParams{
		ScreenName: u,
	})
	for t := range user {

		ioutil.WriteFile("partys/"+p+"/"+u+"/"+user[t].IDStr+".TXT", []byte(user[t].Text), 0755)
	}
	fmt.Println(u)
	wg.Done()
}

func main() {
	fmt.Println("Hello")

	config := oauth1.NewConfig("EOrXKkxg0XzFzlFOTA3jDAs4f", "MOpd38qVPPL2okboPfRh8zydfLRFmy3mulB5LhQv1xKKsfMHRh")
	token := oauth1.NewToken("388252133-aVIPGzoy8D19TP4QdBBhV0zlOMlmwcoSOt760KRs", "obs8ggbMMlULwijO3PCAhqDRn8joUssOEsaQHyi5uF10r")
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
