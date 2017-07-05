package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
	"github.com/gorilla/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"sync"
)

var clientsMutex = sync.Mutex{}

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
	fmt.Println(os.Getenv("CONSUMER_KEY"))
	config := oauth1.NewConfig(os.Getenv("CONSUMER_KEY"), os.Getenv("CONSUMER_SECRET"))
	token := oauth1.NewToken(os.Getenv("ACCESS_TOKEN_KEY"), os.Getenv("ACCESS_TOKEN_SECRET"))
	// OAuth1 http.Client will automatically authorize Requests
	httpClient := config.Client(oauth1.NoContext, token)

	// Twitter Client
	client := twitter.NewClient(httpClient)

	demux := twitter.NewSwitchDemux()
	demux.Tweet = func(tweet *twitter.Tweet) {
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
			Profile_img:  tweet.User.ProfileImageURL,
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
		broadcast(msg_rdy)

	}

	fmt.Println("Starting Stream...")
	// USER (quick test: auth'd user likes a tweet -> event)
	userParams := &twitter.StreamUserParams{
		StallWarnings: twitter.Bool(true),
		With:          "followings",
	}
	stream, err := client.Streams.User(userParams)
	if err != nil {
		log.Fatal(err)
	}

	// Receive messages until stopped or stream quits
	go demux.HandleChan(stream.Messages)
}

func echo(w http.ResponseWriter, r *http.Request) {

	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("upgrade:", err)
		return
	}
	fmt.Println("Websocket connected")
	sub := subscribe()

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
	log.Fatal(http.ListenAndServe("0.0.0.0:8001", nil))
}
