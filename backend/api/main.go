package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/ChimeraCoder/anaconda"
	"github.com/gorilla/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"sync"
)

var clientsMutex = sync.Mutex{}
var tweetHistoryMutex = sync.Mutex{}

var lastmsgs [5][]byte

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type ws_msg struct {
	Profile_img  string `json:"profile_img"`
	Name         string `json:"name"`
	Handle       string `json:"handle"`
	Text         string `json:"text"`
	Date         string `json:"date"`
	RealParty    string `json:"real_party"`
	GuessedParty string `json:"guessed_party"`
}

var clients []chan []byte

func subscribe() chan []byte {
	sub := make(chan []byte)
	clientsMutex.Lock()
	clients = append(clients, sub)
	clientsMutex.Unlock()
	return sub
}

func unsubscribe(sub chan []byte) {
	clientsMutex.Lock()
	newSubs := []chan []byte{}
	subs := clients
	for _, s := range subs {
		if s != sub {
			newSubs = append(newSubs, s)
		}
	}
	clients = newSubs
	clientsMutex.Unlock()
}

func broadcast(msg []byte) {
	clientsMutex.Lock()
	for _, c := range clients {
		c <- msg
	}
	clientsMutex.Unlock()
}

func t_stream(data map[string]string) {
	fmt.Println("Config")
	consumer_key := os.Getenv("CONSUMER_KEY")
	consumer_secret := os.Getenv("CONSUMER_SECRET")
	access_token := os.Getenv("ACCESS_TOKEN_KEY")
	access_token_secret := os.Getenv("ACCESS_TOKEN_SECRET")

	anaconda.SetConsumerKey(consumer_key[:len(consumer_key)-1])
	anaconda.SetConsumerSecret(consumer_secret[:len(consumer_secret)-1])
	api := anaconda.NewTwitterApi(access_token[:len(access_token)-1], access_token_secret[:len(access_token_secret)-1])
	fmt.Println(consumer_key)
	ok, err := api.VerifyCredentials()

	if err != nil {
		panic(err)
	}
	if !ok {
		panic("Login failed")
	}

	fmt.Println("Starting Stream...")

	options := url.Values{}
	options.Set("StallWarnings", "true")
	options.Set("With", "followings")
	s := api.UserStream(options)

	for {
		item := <-s.C
		switch tweet := item.(type) {
		case anaconda.Tweet:
			fmt.Println(tweet.Text)
			cmd := exec.Command("python3", "predict.py", "\""+tweet.Text+"\"")
			var out bytes.Buffer
			cmd.Stdout = &out
			err := cmd.Run()
			if err != nil {
				fmt.Println(out.String())
				log.Fatal(err)
			}

			msg := ws_msg{
				Profile_img:  tweet.User.ProfileImageUrlHttps,
				Name:         tweet.User.Name,
				Handle:       tweet.User.ScreenName,
				Text:         tweet.Text,
				Date:         tweet.CreatedAt,
				RealParty:    data[tweet.User.ScreenName],
				GuessedParty: out.String(),
			}

			fmt.Println("Raw Struct", msg)
			msg_rdy, err := json.Marshal(msg)
			if err != nil {
				fmt.Println("Err JSON Marshal", err)
			}
			tweetHistoryMutex.Lock()
			var newmsgs [5][]byte
			for i, _ := range lastmsgs {
				if i != 4 {
					newmsgs[i] = lastmsgs[i+1]
				} else {
					newmsgs[4] = msg_rdy
				}
			}
			lastmsgs = newmsgs

			tweetHistoryMutex.Unlock()
			broadcast(msg_rdy)
		default:

		}
	}
}

func echo(w http.ResponseWriter, r *http.Request) {

	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("upgrade:", err)
		return
	}
	fmt.Println("Websocket connected")
	sub := subscribe()
	tweetHistoryMutex.Lock()
	for _, t := range lastmsgs {
		if t != nil {
			err := c.WriteMessage(websocket.TextMessage, t)
			if err != nil {
				break
			}
		}
	}
	tweetHistoryMutex.Unlock()
	for {
		message := <-sub
		err := c.WriteMessage(websocket.TextMessage, message)
		if err != nil {
			break
		}

	}
	unsubscribe(sub)
	fmt.Println("Client disconnected")
}

func main() {
	var data map[string]string
	mdbs_bytes, _ := ioutil.ReadFile("mdbs_twitter.json")
	json.Unmarshal(mdbs_bytes, &data)

	go t_stream(data)
	http.HandleFunc("/", echo)
	address := "0.0.0.0:8001"
	if os.Getenv("ENV") == "dev" {
		address = "127.0.0.1:8010"
		fmt.Println("Starting up dev enviroment")
	}
	log.Fatal(http.ListenAndServe(address, nil))
}
